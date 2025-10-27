const API_BASE = "http://127.0.0.1:8000"; // FastAPI backend

// =================== REGISTER ===================
const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
  name: document.getElementById("name").value,
  email: document.getElementById("email").value,
  password: document.getElementById("password").value,
  role: document.getElementById("role").value,
};

    // ✅ Use correct endpoint
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (res.ok) {
      alert("✅ Registration successful! Please login.");
      window.location.href = "login.html";
    } else {
      try {
        const err = await res.json();
        console.error("Registration error:", err);
        alert("❌ Registration failed: " + JSON.stringify(err));

      } catch {
        alert("❌ Registration failed: " + res.statusText);
      }
    }
  });
}

// =================== LOGIN ===================
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
      email: document.getElementById("loginEmail").value,
      password: document.getElementById("loginPassword").value,
    };

    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await res.json();

    if (res.ok) {
      localStorage.setItem("token", result.access_token);
      localStorage.setItem("role", result.user_role);
      localStorage.setItem("username", result.user);

      alert("✅ Login successful!");

      if (result.user_role === "admin") {
        window.location.href = "dashboard_admin.html";
      } else if (result.user_role === "manager") {
        window.location.href = "dashboard_manager.html";
      } else {
        window.location.href = "dashboard_developer.html";
      }
    } else {
      alert("❌ Invalid credentials: " + (result.detail || "Try again"));
    }
  });
}

// =================== LOGOUT ===================
function logout() {
  console.log("Logout function called"); // ✅ For debugging
  alert("Logging out...");
  localStorage.clear();
  window.location.href = "login.html";
}



// Show/hide task form
const showTaskBtn = document.getElementById("showTaskForm");
if (showTaskBtn) {
  showTaskBtn.addEventListener("click", () => {
    document.getElementById("taskForm").style.display = "block";
  });
}

// Assign Task
const assignBtn = document.getElementById("assignTask");
if (assignBtn) {
  assignBtn.addEventListener("click", async () => {
    const token = localStorage.getItem("token");

    const task = {
      title: document.getElementById("title").value,
      description: document.getElementById("description").value,
      project_id: Number(document.getElementById("project_id").value),
      assignee_id: Number(document.getElementById("assignee_id").value),
      deadline: document.getElementById("deadline").value,
    };

    const res = await fetch(`${API_BASE}/tasks/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify(task),
    });

    if (res.ok) {
      alert("✅ Task assigned successfully!");
      document.getElementById("taskForm").reset();
    } else {
      const err = await res.json();
      alert("❌ Failed to assign task: " + err.detail);
    }
  });
}
