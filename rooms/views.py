from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Room, RoomParticipant
from .forms import RoomCreationForm, JoinRoomForm, RoomEditForm, RoomSettingsForm
from accounts.models import User
import json


@login_required
def room_list(request):
    """List all rooms based on user role"""
    if request.user.role == 'teacher':
        rooms = Room.objects.filter(teacher=request.user).order_by('-created_at')
    else:
        # Students see rooms they've joined
        rooms = Room.objects.filter(participants__student=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'rooms': page_obj,
        'total_rooms': rooms.count(),
    }
    return render(request, 'rooms/room_list.html', context)


@login_required
def create_room(request):
    """Create a new room (teachers only)"""
    if request.user.role != 'teacher':
        messages.error(request, "Access denied. Only teachers can create rooms.")
        return redirect('room_list')
    
    if request.method == 'POST':
        form = RoomCreationForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.teacher = request.user
            
            # Parse settings if provided
            settings = form.cleaned_data.get('settings')
            if settings:
                try:
                    room.settings = json.loads(settings)
                except json.JSONDecodeError:
                    room.settings = {}
            
            room.save()
            messages.success(request, f"Room '{room.name}' created successfully! Invite code: {room.invite_code}")
            return redirect('room_detail', room_id=room.id)
    else:
        form = RoomCreationForm()
    
    context = {
        'form': form,
        'title': 'Create New Room',
    }
    return render(request, 'rooms/create_room.html', context)


@login_required
def room_detail(request, room_id):
    """View room details"""
    room = get_object_or_404(Room, id=room_id)
    
    # Check permissions
    if request.user.role == 'teacher' and room.teacher != request.user:
        messages.error(request, "Access denied. You can only view your own rooms.")
        return redirect('room_list')
    elif request.user.role == 'student' and not room.participants.filter(student=request.user).exists():
        messages.error(request, "Access denied. You must join this room first.")
        return redirect('room_list')
    
    participants = room.participants.all().order_by('joined_at')
    
    # Check if room has a test
    has_test = hasattr(room, 'test') and room.test is not None
    
    context = {
        'room': room,
        'participants': participants,
        'has_test': has_test,
        'is_teacher': request.user.role == 'teacher',
        'is_participant': room.participants.filter(student=request.user).exists(),
    }
    return render(request, 'rooms/room_detail.html', context)


@login_required
def join_room(request, room_id):
    """Join a room by ID (for students)"""
    room = get_object_or_404(Room, id=room_id)
    
    if request.user.role != 'student':
        messages.error(request, "Access denied. Only students can join rooms.")
        return redirect('room_detail', room_id=room_id)
    
    # Check if room is active
    if not room.is_active:
        messages.error(request, "This room is no longer active.")
        return redirect('room_list')
    
    # Check if room is full
    if room.is_full:
        messages.error(request, "This room is full.")
        return redirect('room_list')
    
    # Check if already joined
    if room.participants.filter(student=request.user).exists():
        messages.info(request, "You are already in this room.")
        return redirect('room_detail', room_id=room_id)
    
    # Check deadline
    is_late = timezone.now() > room.entry_deadline
    
    if is_late and not room.settings.get('allow_late_entry', False):
        messages.error(request, "The entry deadline for this room has passed.")
        return redirect('room_list')
    
    # Join the room
    participant = RoomParticipant.objects.create(
        room=room,
        student=request.user,
        is_late=is_late,
        penalty_applied=room.late_penalty if is_late else 0.0
    )
    
    if is_late:
        messages.warning(request, f"You joined late. A penalty of {room.late_penalty} will be applied.")
    else:
        messages.success(request, f"Successfully joined room '{room.name}'!")
    
    return redirect('room_detail', room_id=room_id)


@login_required
def join_room_by_code(request, invite_code=None):
    """Join a room using invite code"""
    if request.user.role != 'student':
        messages.error(request, "Access denied. Only students can join rooms.")
        return redirect('room_list')
    
    if request.method == 'POST':
        form = JoinRoomForm(request.POST)
        if form.is_valid():
            invite_code = form.cleaned_data['invite_code']
            try:
                room = Room.objects.get(invite_code=invite_code)
                return redirect('join_room', room_id=room.id)
            except Room.DoesNotExist:
                messages.error(request, "Invalid invite code.")
    else:
        form = JoinRoomForm()
        if invite_code:
            form.initial['invite_code'] = invite_code
    
    context = {
        'form': form,
        'title': 'Join Room',
    }
    return render(request, 'rooms/join_room.html', context)


@login_required
def edit_room(request, room_id):
    """Edit room details (teachers only)"""
    room = get_object_or_404(Room, id=room_id)
    
    if request.user.role != 'teacher' or room.teacher != request.user:
        messages.error(request, "Access denied. You can only edit your own rooms.")
        return redirect('room_detail', room_id=room_id)
    
    if request.method == 'POST':
        form = RoomEditForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated successfully!")
            return redirect('room_detail', room_id=room_id)
    else:
        form = RoomEditForm(instance=room)
    
    context = {
        'form': form,
        'room': room,
        'title': f'Edit Room: {room.name}',
    }
    return render(request, 'rooms/edit_room.html', context)


@login_required
def remove_participant(request, room_id, participant_id):
    """Remove a participant from the room (teachers only)"""
    room = get_object_or_404(Room, id=room_id)
    participant = get_object_or_404(RoomParticipant, id=participant_id, room=room)
    
    if request.user.role != 'teacher' or room.teacher != request.user:
        messages.error(request, "Access denied. You can only remove participants from your own rooms.")
        return redirect('room_detail', room_id=room_id)
    
    if request.method == 'POST':
        student_name = participant.student.username
        participant.delete()
        messages.success(request, f"Removed {student_name} from the room.")
        return redirect('room_detail', room_id=room_id)
    
    context = {
        'room': room,
        'participant': participant,
    }
    return render(request, 'rooms/remove_participant.html', context)


@login_required
def leave_room(request, room_id):
    """Leave a room (students only)"""
    room = get_object_or_404(Room, id=room_id)
    
    if request.user.role != 'student':
        messages.error(request, "Access denied. Only students can leave rooms.")
        return redirect('room_detail', room_id=room_id)
    
    try:
        participant = RoomParticipant.objects.get(room=room, student=request.user)
        
        if request.method == 'POST':
            participant.delete()
            messages.success(request, f"You have left the room '{room.name}'.")
            return redirect('room_list')
        
        context = {
            'room': room,
            'participant': participant,
        }
        return render(request, 'rooms/leave_room.html', context)
        
    except RoomParticipant.DoesNotExist:
        messages.error(request, "You are not in this room.")
        return redirect('room_list')
