const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
            ...(options.headers || {})
        },
        credentials: "same-origin"
    });
    let data = null;
    if (response.status !== 204) {
        data = await response.json().catch(() => null);
    }
    if (!response.ok) {
        const errorMsg = data?.detail || data?.error || JSON.stringify(data);
        throw new Error(errorMsg || "Ошибка выполнения запроса");
    }
    return data;
}

function showMessage(text, isError = false) {
    const msgEl = document.getElementById("message");
    msgEl.textContent = text;
    msgEl.className = "alert " + (isError ? "alert-danger" : "alert-success");
    setTimeout(() => { msgEl.textContent = ""; msgEl.className = ""; }, 4000);
}

const roomSelect = document.getElementById("room");
const roomFilter = document.getElementById("room-filter");
const form = document.getElementById("booking-form");
const purposeInput = document.getElementById("purpose");
const list = document.getElementById("bookings-list");
const loading = document.getElementById("loading");
const statusFilter = document.getElementById("status-filter");

async function loadRooms() {
    const rooms = await apiRequest("/bookings/api/rooms/");
    roomSelect.replaceChildren();
    roomFilter.replaceChildren();
    roomFilter.innerHTML = '<option value="">Все комнаты</option>';

    rooms.forEach(room => {
        const opt1 = document.createElement("option");
        opt1.value = room.id;
        opt1.textContent = `${room.name} (Вместимость: ${room.capacity})`;
        if (!room.is_available) opt1.textContent += " [ЗАНЯТА]";
        roomSelect.append(opt1);

        const opt2 = document.createElement("option");
        opt2.value = room.id;
        opt2.textContent = room.name;
        roomFilter.append(opt2);
    });
}

async function loadBookings() {
    loading.hidden = false;
    const params = new URLSearchParams();
    if (statusFilter.value) params.set("status", statusFilter.value);
    if (roomFilter.value) params.set("room", roomFilter.value);

    const query = params.toString();
    const url = "/bookings/api/bookings/" + (query ? "?" + query : "");

    try {
        const bookings = await apiRequest(url);
        list.replaceChildren();
        if (bookings.length === 0) {
            list.innerHTML = '<p class="text-muted text-center">Бронирования не найдены</p>';
            return;
        }

        bookings.forEach(booking => {
            const row = document.createElement("div");
            row.className = "card mb-2 p-3";

            let actions = "";
            if (booking.status === "created") {
                actions = `
                    <button class="btn btn-sm btn-success" onclick="changeStatus(${booking.id}, 'approve')">Подтвердить</button>
                    <button class="btn btn-sm btn-danger" onclick="changeStatus(${booking.id}, 'reject')">Отклонить</button>
                `;
            } else if (booking.status === "approved") {
                actions = `<button class="btn btn-sm btn-primary" onclick="changeStatus(${booking.id}, 'complete')">Завершить</button>`;
            }

            let historyHtml = "";
            if (booking.history && booking.history.length > 0) {
                historyHtml = "<ul class='mt-2 mb-0 small text-muted'>";
                booking.history.forEach(h => {
                    historyHtml += `<li>${h.action} (${h.timestamp}) — ${h.user_username}</li>`;
                });
                historyHtml += "</ul>";
            }

            row.innerHTML = `
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <strong>${booking.room_name}</strong> <span class="badge status-${booking.status}">${booking.status}</span>
                        <div class="small text-muted">Цель: ${booking.purpose}</div>
                        ${historyHtml}
                    </div>
                    <div class="d-flex flex-column gap-2">
                        ${actions}
                        <button class="btn btn-sm btn-outline-secondary" onclick="deleteBooking(${booking.id}, '${booking.room_name}')">Удалить</button>
                    </div>
                </div>
            `;
            list.append(row);
        });
    } catch (error) {
        showMessage("Ошибка загрузки: " + error.message, true);
    } finally {
        loading.hidden = true;
    }
}

async function changeStatus(id, action) {
    try {
        await apiRequest(`/bookings/api/bookings/${id}/${action}/`, { method: "POST" });
        showMessage("Статус успешно изменен");
        await loadBookings();
    } catch (error) {
        showMessage("Ошибка: " + error.message, true);
    }
}

async function deleteBooking(id, name) {
    if (!confirm(`Удалить бронь "${name}"?`)) return;
    try {
        await apiRequest(`/bookings/api/bookings/${id}/`, { method: "DELETE" });
        showMessage("Бронирование удалено");
        await loadBookings();
    } catch (error) {
        showMessage("Ошибка удаления: " + error.message, true);
    }
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        await apiRequest("/bookings/api/bookings/", {
            method: "POST",
            body: JSON.stringify({
                purpose: purposeInput.value,
                room: Number(roomSelect.value)
            })
        });
        purposeInput.value = "";
        showMessage("Бронирование успешно создано");
        await loadBookings();
    } catch (error) {
        showMessage("Ошибка создания: " + error.message, true);
    }
});

statusFilter.addEventListener("change", loadBookings);
roomFilter.addEventListener("change", loadBookings);

async function initialize() {
    try {
        await loadRooms();
        await loadBookings();
    } catch (error) {
        showMessage("Ошибка инициализации: " + error.message, true);
    }
}
initialize();