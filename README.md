# 💪 Gym Management System — FastAPI

A complete **Gym Management System** backend built with **FastAPI** as part of the Innomatics Research Labs FastAPI Internship (IN226095802).

---

## 🚀 Features Implemented

| Day | Concept | Details |
|-----|---------|---------|
| Day 1 | GET APIs | Home route, list members, get by ID, summary stats |
| Day 2 | POST + Pydantic | Add member with full field validation & constraints |
| Day 3 | Helper Functions | `find_member()`, `find_trainer()`, `calculate_plan_price()`, `filter_members()` |
| Day 4 | CRUD Operations | PUT (update member/equipment), DELETE (remove member) |
| Day 5 | Multi-Step Workflow | Book Session → Check-In → Process Payment |
| Day 6 | Advanced APIs | Search, Sort, Pagination, Combined Browse |

---

## 📋 All 20 Endpoints

| # | Method | Route | Description |
|---|--------|-------|-------------|
| Q1  | GET    | `/`                          | Home / Welcome route |
| Q2  | GET    | `/members`                   | List all members |
| Q3  | GET    | `/members/{member_id}`       | Get member by ID |
| Q4  | GET    | `/members/summary/stats`     | Members summary & stats |
| Q5  | POST   | `/members`                   | Add new member (Pydantic validated) |
| Q6  | GET    | `/trainers`                  | List all trainers |
| Q7  | GET    | `/plans/price`               | Get plan price (helper function) |
| Q8  | PUT    | `/members/{member_id}`       | Update member details |
| Q9  | DELETE | `/members/{member_id}`       | Delete a member |
| Q10 | PUT    | `/equipment/{equipment_id}`  | Update equipment details |
| Q11 | POST   | `/sessions/book`             | Book a training session (Workflow Step 1) |
| Q12 | POST   | `/checkin/{member_id}`       | Member check-in (Workflow Step 2) |
| Q13 | POST   | `/payments`                  | Process payment (Workflow Step 3) |
| Q14 | GET    | `/sessions`                  | View all sessions |
| Q15 | GET    | `/checkins`                  | View all check-ins |
| Q16 | GET    | `/equipment`                 | List all equipment |
| Q17 | GET    | `/members/search/query`      | Search members (Day 6) |
| Q18 | GET    | `/members/sort/results`      | Sort members (Day 6) |
| Q19 | GET    | `/members/page/list`         | Paginate members (Day 6) |
| Q20 | GET    | `/members/browse/all`        | Combined browse: filter + sort + paginate (Day 6) |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI 0.111.0**
- **Pydantic v2**
- **Uvicorn** (ASGI server)

---

## ⚙️ Setup & Run

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/fastapi-gym-management-system.git
cd fastapi-gym-management-system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn main:app --reload

# 5. Open Swagger UI
# http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure

```
fastapi-gym-management-system/
├── main.py               # All 20 FastAPI endpoints
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── screenshots/          # Swagger UI screenshots (Q1–Q20)
```

---

## 🔄 Multi-Step Workflow (Day 5)

```
Book Session  →  Check-In  →  Process Payment
POST /sessions/book   POST /checkin/{id}   POST /payments
```

---

## 🔍 Advanced Features (Day 6)

- **Search**: `/members/search/query?name=aarav&plan=monthly&active=true`
- **Sort**: `/members/sort/results?sort_by=age&order=desc`
- **Paginate**: `/members/page/list?page=1&per_page=2`
- **Combined**: `/members/browse/all?name=a&sort_by=age&order=asc&page=1&per_page=2`

---

## 👨‍💻 Author

**Sri Vinay Vatti** | Intern ID: IN226095802
Innomatics Research Labs — FastAPI Internship

---

## 🏷️ Tags

`#FastAPI` `#Python` `#BackendDevelopment` `#APIDevelopment` `#GymManagement` `#InnomaticsResearchLabs`
