"""
FSM (Finite State Machine) states for the booking flow.

States define the user's position in the multi-step booking conversation:
  1. Choose service
  2. Choose staff (barber)
  3. Choose date
  4. Choose time slot
  5. Confirm booking

aiogram's FSM tracks which step each user is on,
so multiple users can book simultaneously without interference.
"""

from aiogram.fsm.state import State, StatesGroup


class BookingStates(StatesGroup):
    """States for the client booking flow."""

    choosing_service = State()   # User is picking a service
    choosing_staff = State()     # User is picking a barber
    choosing_date = State()      # User is picking a date
    choosing_time = State()      # User is picking a time slot
    confirming = State()         # User is confirming the booking
