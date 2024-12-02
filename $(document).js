   $(document).ready(function() {
       $.get('path/to/your/api/schedule', function(data) {
           const tbody = $('#scheduleTable tbody');
           data.forEach(item => {
               tbody.append(`<tr><td>${item.date}</td><td>${item.time}</td><td>${item.instructor}</td></tr>`);
           });
       });
   });
   document.getElementById("registration-form").addEventListener("submit", async (event) => {
    event.preventDefault(); // Предотвращаем стандартное поведение отправки формы
  
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const courseDate = document.getElementById("course-date").value;
  
    // Простая клиентская валидация
    if (!name || !email || !phone || !courseDate) {
      alert("Пожалуйста, заполните все поля.");
      return;
    }
  
    if (!/^\+?[0-9]{10,15}$/.test(phone)) {
      alert("Введите корректный номер телефона.");
      return;
    }
  
    const requestData = {
      name,
      email,
      phone,
      courseDate,
    };
  
    try {
      const response = await fetch("https://api.example.com/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });
  
      const result = await response.json();
      if (response.ok) {
        document.getElementById("response-message").textContent = "Регистрация успешна!";
      } else {
        document.getElementById("response-message").textContent = "Ошибка: ${result.message}";
      }
    } catch (error) {
      document.getElementById("response-message").textContent = "Ошибка при отправке данных. Попробуйте позже.";
    }
  });