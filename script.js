// SIGNUP
const signupForm = document.getElementById("signupForm");

if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const res = await fetch("/api/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();
        document.getElementById("message").textContent = data.message;

        if (data.status === "success") {
            localStorage.setItem("role, data.role");
            window.location.href = "login.html";
        }
    });
}

// LOGIN
const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password, role: document.getElementById("role").value })
        });

        const data = await res.json();

        if (data.status === "success") {
            localStorage.setItem("workerEmail", email);
            localStorage.setItem("role", data.role);
        
         if (data.role === "admin") {
           window.location.href = "admin.html";
          }
         else if (data.role === "company") {
           window.location.href = "company.html";
         }
         else {
         // worker
           window.location.href = "dashboard.html";
         }   
         
                 if (data.role === "admin") {
           window.location.href = "admin.html";
         }
        } else {
            document.getElementById("loginMessage").textContent = "Login failed";
        }
    });
}

const email = localStorage.getItem("workerEmail");

// Load tasks
fetch("/api/tasks")
  .then(res => res.json())
  .then(tasks => {
    const list = document.getElementById("tasks");
    list.innerHTML = "";

    tasks.forEach(task => {
      const li = document.createElement("li");

      const btn = document.createElement("button");
      btn.textContent = "Complete";
      btn.onclick = () => completeTask(task);

      li.innerHTML = `<strong>${task.title}</strong> - $${task.pay} `;
      li.appendChild(btn);

      list.appendChild(li);
    });
  });

// Complete task
function completeTask(task) {
  fetch("/api/complete-task", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: email,
      title: task.title,
      pay: task.pay
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "success") {
      document.getElementById("earnings").textContent =
        "$" + data.earnings.toFixed(2);

      const completedList = document.getElementById("completed");
      const li = document.createElement("li");
      li.textContent = task.title;
      completedList.appendChild(li);
    }
  });
}
function logout() {
  localStorage.clear();
  window.location.href = "login.html";
}
