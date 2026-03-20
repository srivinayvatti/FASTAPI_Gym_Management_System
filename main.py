from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

app = FastAPI(
    title="Gym Management System",
    description="A complete Gym Management backend built with FastAPI",
    version="1.0.0"
)

# ─────────────────────────────────────────────
# In-memory Data Store
# ─────────────────────────────────────────────

members = [
    {"id": 1, "name": "Aarav Sharma",   "age": 25, "email": "aarav@gym.com",   "plan": "monthly",  "active": True,  "join_date": "2024-01-10"},
    {"id": 2, "name": "Priya Mehta",    "age": 30, "email": "priya@gym.com",   "plan": "quarterly","active": True,  "join_date": "2024-02-15"},
    {"id": 3, "name": "Rohan Patil",    "age": 22, "email": "rohan@gym.com",   "plan": "monthly",  "active": False, "join_date": "2024-03-01"},
    {"id": 4, "name": "Sneha Kulkarni", "age": 27, "email": "sneha@gym.com",   "plan": "yearly",   "active": True,  "join_date": "2024-01-20"},
    {"id": 5, "name": "Karan Joshi",    "age": 35, "email": "karan@gym.com",   "plan": "monthly",  "active": True,  "join_date": "2024-04-05"},
]

trainers = [
    {"id": 1, "name": "Vikram Singh",  "specialty": "Strength Training", "experience_years": 8,  "available": True},
    {"id": 2, "name": "Neha Desai",    "specialty": "Yoga & Flexibility","experience_years": 5,  "available": True},
    {"id": 3, "name": "Amit Rao",      "specialty": "Cardio & HIIT",     "experience_years": 6,  "available": False},
    {"id": 4, "name": "Pooja Nair",    "specialty": "CrossFit",          "experience_years": 4,  "available": True},
]

equipment = [
    {"id": 1, "name": "Treadmill",      "quantity": 10, "condition": "good",      "category": "cardio"},
    {"id": 2, "name": "Dumbbells Set",  "quantity": 20, "condition": "excellent", "category": "strength"},
    {"id": 3, "name": "Barbell Rack",   "quantity": 5,  "condition": "good",      "category": "strength"},
    {"id": 4, "name": "Rowing Machine", "quantity": 4,  "condition": "fair",      "category": "cardio"},
    {"id": 5, "name": "Yoga Mats",      "quantity": 30, "condition": "good",      "category": "flexibility"},
]

sessions = []        # booked sessions
checkins  = []       # check-in records
payments  = []       # payment records

member_id_counter   = 6
session_id_counter  = 1
checkin_id_counter  = 1
payment_id_counter  = 1

# ─────────────────────────────────────────────
# Pydantic Models
# ─────────────────────────────────────────────

class MemberCreate(BaseModel):
    name:       str         = Field(..., min_length=2, max_length=100)
    age:        int         = Field(..., ge=15, le=80)
    email:      str         = Field(..., min_length=5)
    plan:       str         = Field(..., pattern="^(monthly|quarterly|yearly)$")

class MemberUpdate(BaseModel):
    name:       Optional[str] = Field(None, min_length=2, max_length=100)
    age:        Optional[int] = Field(None, ge=15, le=80)
    plan:       Optional[str] = Field(None, pattern="^(monthly|quarterly|yearly)$")
    active:     Optional[bool] = None

class SessionBook(BaseModel):
    member_id:  int         = Field(..., ge=1)
    trainer_id: int         = Field(..., ge=1)
    session_date: str       = Field(..., description="YYYY-MM-DD")
    session_type: str       = Field(..., pattern="^(strength|cardio|yoga|crossfit|hiit)$")
    duration_mins: int      = Field(..., ge=30, le=180)

class PaymentCreate(BaseModel):
    member_id:  int         = Field(..., ge=1)
    amount:     float       = Field(..., gt=0)
    plan:       str         = Field(..., pattern="^(monthly|quarterly|yearly)$")

class EquipmentUpdate(BaseModel):
    quantity:   Optional[int] = Field(None, ge=0)
    condition:  Optional[str] = Field(None, pattern="^(excellent|good|fair|poor)$")

# ─────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────

def find_member(member_id: int):
    return next((m for m in members if m["id"] == member_id), None)

def find_trainer(trainer_id: int):
    return next((t for t in trainers if t["id"] == trainer_id), None)

def find_equipment(equipment_id: int):
    return next((e for e in equipment if e["id"] == equipment_id), None)

def calculate_plan_price(plan: str) -> float:
    prices = {"monthly": 999.0, "quarterly": 2699.0, "yearly": 9999.0}
    return prices.get(plan, 0.0)

def filter_members(name=None, plan=None, active=None):
    result = members
    if name    is not None: result = [m for m in result if name.lower() in m["name"].lower()]
    if plan    is not None: result = [m for m in result if m["plan"] == plan]
    if active  is not None: result = [m for m in result if m["active"] == active]
    return result

# ─────────────────────────────────────────────
# Q1 — Home / Welcome Route  (Day 1 GET)
# ─────────────────────────────────────────────
@app.get("/", tags=["General"])
def home():
    return {
        "message": "💪 Welcome to Gym Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# ─────────────────────────────────────────────
# Q2 — List All Members  (Day 1 GET)
# ─────────────────────────────────────────────
@app.get("/members", tags=["Members"])
def get_all_members():
    return {"total": len(members), "members": members}

# ─────────────────────────────────────────────
# Q3 — Get Member by ID  (Day 1 GET)
# ─────────────────────────────────────────────
@app.get("/members/{member_id}", tags=["Members"])
def get_member_by_id(member_id: int):
    member = find_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail=f"Member with ID {member_id} not found")
    return member

# ─────────────────────────────────────────────
# Q4 — Members Summary / Count  (Day 1 GET)
# ─────────────────────────────────────────────
@app.get("/members/summary/stats", tags=["Members"])
def members_summary():
    active_count   = sum(1 for m in members if m["active"])
    inactive_count = len(members) - active_count
    plan_counts    = {}
    for m in members:
        plan_counts[m["plan"]] = plan_counts.get(m["plan"], 0) + 1
    return {
        "total_members":    len(members),
        "active_members":   active_count,
        "inactive_members": inactive_count,
        "plan_breakdown":   plan_counts
    }

# ─────────────────────────────────────────────
# Q5 — Add New Member  (Day 2 POST + Pydantic)
# ─────────────────────────────────────────────
@app.post("/members", status_code=201, tags=["Members"])
def add_member(member: MemberCreate):
    global member_id_counter
    # Check duplicate email
    if any(m["email"] == member.email for m in members):
        raise HTTPException(status_code=400, detail="Email already registered")
    new_member = {
        "id":        member_id_counter,
        "name":      member.name,
        "age":       member.age,
        "email":     member.email,
        "plan":      member.plan,
        "active":    True,
        "join_date": str(date.today())
    }
    members.append(new_member)
    member_id_counter += 1
    return {"message": "Member registered successfully", "member": new_member}

# ─────────────────────────────────────────────
# Q6 — List All Trainers  (Day 1 GET)
# ─────────────────────────────────────────────
@app.get("/trainers", tags=["Trainers"])
def get_all_trainers():
    return {"total": len(trainers), "trainers": trainers}

# ─────────────────────────────────────────────
# Q7 — Get Plan Price  (Day 3 Helper Function)
# ─────────────────────────────────────────────
@app.get("/plans/price", tags=["Plans"])
def get_plan_price(plan: str = Query(..., pattern="^(monthly|quarterly|yearly)$")):
    price = calculate_plan_price(plan)
    return {
        "plan":     plan,
        "price_inr": price,
        "description": f"₹{price} for {plan} membership"
    }

# ─────────────────────────────────────────────
# Q8 — Update Member  (Day 4 CRUD - PUT)
# ─────────────────────────────────────────────
@app.put("/members/{member_id}", tags=["Members"])
def update_member(member_id: int, updates: MemberUpdate):
    member = find_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail=f"Member with ID {member_id} not found")
    if updates.name   is not None: member["name"]   = updates.name
    if updates.age    is not None: member["age"]    = updates.age
    if updates.plan   is not None: member["plan"]   = updates.plan
    if updates.active is not None: member["active"] = updates.active
    return {"message": "Member updated successfully", "member": member}

# ─────────────────────────────────────────────
# Q9 — Delete Member  (Day 4 CRUD - DELETE)
# ─────────────────────────────────────────────
@app.delete("/members/{member_id}", tags=["Members"])
def delete_member(member_id: int):
    member = find_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail=f"Member with ID {member_id} not found")
    members.remove(member)
    return {"message": f"Member '{member['name']}' deleted successfully"}

# ─────────────────────────────────────────────
# Q10 — Update Equipment  (Day 4 CRUD - PUT)
# ─────────────────────────────────────────────
@app.put("/equipment/{equipment_id}", tags=["Equipment"])
def update_equipment(equipment_id: int, updates: EquipmentUpdate):
    item = find_equipment(equipment_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Equipment with ID {equipment_id} not found")
    if updates.quantity  is not None: item["quantity"]  = updates.quantity
    if updates.condition is not None: item["condition"] = updates.condition
    return {"message": "Equipment updated successfully", "equipment": item}

# ─────────────────────────────────────────────
# Q11 — Book a Session  (Day 5 Workflow - Step 1)
# ─────────────────────────────────────────────
@app.post("/sessions/book", status_code=201, tags=["Workflow: Sessions"])
def book_session(session: SessionBook):
    global session_id_counter
    member = find_member(session.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if not member["active"]:
        raise HTTPException(status_code=400, detail="Inactive members cannot book sessions")
    trainer = find_trainer(session.trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    if not trainer["available"]:
        raise HTTPException(status_code=400, detail=f"Trainer '{trainer['name']}' is currently unavailable")
    new_session = {
        "session_id":    session_id_counter,
        "member_id":     session.member_id,
        "member_name":   member["name"],
        "trainer_id":    session.trainer_id,
        "trainer_name":  trainer["name"],
        "session_date":  session.session_date,
        "session_type":  session.session_type,
        "duration_mins": session.duration_mins,
        "status":        "booked"
    }
    sessions.append(new_session)
    session_id_counter += 1
    return {"message": "Session booked successfully", "session": new_session}

# ─────────────────────────────────────────────
# Q12 — Check-In Member  (Day 5 Workflow - Step 2)
# ─────────────────────────────────────────────
@app.post("/checkin/{member_id}", status_code=201, tags=["Workflow: Sessions"])
def checkin_member(member_id: int):
    global checkin_id_counter
    member = find_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if not member["active"]:
        raise HTTPException(status_code=400, detail="Inactive member cannot check in")
    record = {
        "checkin_id":  checkin_id_counter,
        "member_id":   member_id,
        "member_name": member["name"],
        "checkin_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status":      "checked_in"
    }
    checkins.append(record)
    checkin_id_counter += 1
    return {"message": f"✅ {member['name']} checked in successfully", "record": record}

# ─────────────────────────────────────────────
# Q13 — Process Payment  (Day 5 Workflow - Step 3)
# ─────────────────────────────────────────────
@app.post("/payments", status_code=201, tags=["Workflow: Sessions"])
def process_payment(payment: PaymentCreate):
    global payment_id_counter
    member = find_member(payment.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    expected_price = calculate_plan_price(payment.plan)
    if payment.amount < expected_price:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient payment. Expected ₹{expected_price} for {payment.plan} plan"
        )
    record = {
        "payment_id":  payment_id_counter,
        "member_id":   payment.member_id,
        "member_name": member["name"],
        "plan":        payment.plan,
        "amount_paid": payment.amount,
        "payment_date": str(date.today()),
        "status":      "success"
    }
    payments.append(record)
    # Activate member upon successful payment
    member["active"] = True
    member["plan"]   = payment.plan
    payment_id_counter += 1
    return {"message": "Payment processed successfully", "payment": record}

# ─────────────────────────────────────────────
# Q14 — View All Sessions  (Day 5 - view workflow data)
# ─────────────────────────────────────────────
@app.get("/sessions", tags=["Workflow: Sessions"])
def get_all_sessions():
    return {"total_sessions": len(sessions), "sessions": sessions}

# ─────────────────────────────────────────────
# Q15 — View All Check-Ins  (Day 5 - view workflow data)
# ─────────────────────────────────────────────
@app.get("/checkins", tags=["Workflow: Sessions"])
def get_all_checkins():
    return {"total_checkins": len(checkins), "checkins": checkins}

# ─────────────────────────────────────────────
# Q16 — List All Equipment  (Day 1 GET)
# ─────────────────────────────────────────────
@app.get("/equipment", tags=["Equipment"])
def get_all_equipment():
    return {"total": len(equipment), "equipment": equipment}

# ─────────────────────────────────────────────
# Q17 — Search Members  (Day 6 Advanced - Search)
# ─────────────────────────────────────────────
@app.get("/members/search/query", tags=["Advanced"])
def search_members(
    name:   Optional[str]  = Query(None, description="Search by name"),
    plan:   Optional[str]  = Query(None, description="Filter by plan: monthly/quarterly/yearly"),
    active: Optional[bool] = Query(None, description="Filter by active status")
):
    result = filter_members(name=name, plan=plan, active=active)
    if not result:
        raise HTTPException(status_code=404, detail="No members found matching the criteria")
    return {"total": len(result), "members": result}

# ─────────────────────────────────────────────
# Q18 — Sort Members  (Day 6 Advanced - Sorting)
# ─────────────────────────────────────────────
@app.get("/members/sort/results", tags=["Advanced"])
def sort_members(
    sort_by:  str  = Query("name",  description="Sort by: name, age, join_date"),
    order:    str  = Query("asc",   description="Order: asc or desc")
):
    valid_fields = ["name", "age", "join_date"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"sort_by must be one of {valid_fields}")
    reverse = (order == "desc")
    sorted_members = sorted(members, key=lambda m: m[sort_by], reverse=reverse)
    return {"total": len(sorted_members), "sort_by": sort_by, "order": order, "members": sorted_members}

# ─────────────────────────────────────────────
# Q19 — Paginate Members  (Day 6 Advanced - Pagination)
# ─────────────────────────────────────────────
@app.get("/members/page/list", tags=["Advanced"])
def paginate_members(
    page:     int = Query(1,  ge=1,  description="Page number"),
    per_page: int = Query(2,  ge=1, le=10, description="Items per page")
):
    total       = len(members)
    total_pages = (total + per_page - 1) // per_page
    start       = (page - 1) * per_page
    end         = start + per_page
    paginated   = members[start:end]
    if not paginated:
        raise HTTPException(status_code=404, detail="No members on this page")
    return {
        "page":        page,
        "per_page":    per_page,
        "total":       total,
        "total_pages": total_pages,
        "members":     paginated
    }

# ─────────────────────────────────────────────
# Q20 — Combined Browse Endpoint  (Day 6 Advanced)
# ─────────────────────────────────────────────
@app.get("/members/browse/all", tags=["Advanced"])
def browse_members(
    name:     Optional[str]  = Query(None,  description="Search by name"),
    plan:     Optional[str]  = Query(None,  description="Filter by plan"),
    active:   Optional[bool] = Query(None,  description="Filter by active status"),
    sort_by:  str            = Query("name", description="Sort by: name, age, join_date"),
    order:    str            = Query("asc",  description="asc or desc"),
    page:     int            = Query(1,      ge=1),
    per_page: int            = Query(2,      ge=1, le=10)
):
    # Step 1: Filter
    result = filter_members(name=name, plan=plan, active=active)
    # Step 2: Sort
    valid_fields = ["name", "age", "join_date"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"sort_by must be one of {valid_fields}")
    result = sorted(result, key=lambda m: m[sort_by], reverse=(order == "desc"))
    # Step 3: Paginate
    total       = len(result)
    total_pages = max(1, (total + per_page - 1) // per_page)
    start       = (page - 1) * per_page
    paginated   = result[start:start + per_page]
    return {
        "filters":     {"name": name, "plan": plan, "active": active},
        "sort_by":     sort_by,
        "order":       order,
        "page":        page,
        "per_page":    per_page,
        "total":       total,
        "total_pages": total_pages,
        "members":     paginated
    }
