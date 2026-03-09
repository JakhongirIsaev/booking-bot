"""
FSM (Finite State Machine) states for registration and booking flows.

Registration flow (first-time users):
  1. Choose language
  2. Enter name
  3. Enter phone (optional)

Booking flow:
  1. Choose service
  2. Choose staff (barber)
  3. Choose date
  4. Choose time slot
  5. Confirm booking
"""

from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """States for first-time user registration."""

    choosing_language = State()   # User picks RU / UZ / EN
    entering_name = State()       # User types their name
    entering_phone = State()      # User types phone (optional)


class BookingStates(StatesGroup):
    """States for the client booking flow."""

    choosing_service = State()   # User is picking a service
    choosing_staff = State()     # User is picking a barber
    choosing_date = State()      # User is picking a date
    choosing_time = State()      # User is picking a time slot
    confirming = State()         # User is confirming the booking
