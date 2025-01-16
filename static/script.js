document.addEventListener("DOMContentLoaded", () => {
    const apiBase = "/api/users";
    const levelEndpoint = "/api/levels";
    const tableBody = document.getElementById("user-table-body");
    const addUserButton = document.getElementById("addUserButton");
    const userModal = document.getElementById("userModal");
    const closeModal = document.getElementById("closeModal");
    const userForm = document.getElementById("userForm");
    const modalTitle = document.getElementById("modalTitle");
    let editId = null;

    // Fungsi untuk membuka modal
    const openModal = (isEdit = false, userData = null) => {
        userModal.style.display = "block";
        modalTitle.textContent = isEdit ? "Edit User" : "Tambah User";

        // Jika mode edit, isi data di form
        if (isEdit && userData) {
            document.getElementById("username").value = userData.username;
            document.getElementById("fullname").value = userData.fullname;
            document.getElementById("password").value = ""; // Kosongkan password
            document.getElementById("status").value = userData.status;
            document.getElementById("level_id").value = userData.level_id;
            editId = userData.id; // Simpan ID user yang diedit
        } else {
            userForm.reset();
            editId = null;
        }
    };

    // Fungsi untuk menutup modal
    const closeModalFunction = () => {
        userModal.style.display = "none";
        userForm.reset();
        editId = null;
    };

    // Fungsi untuk memuat data user
    const loadUsers = async () => {
        const token = localStorage.getItem("jwt_token");
        const response = await fetch(apiBase, {
            headers: { Authorization: `Bearer ${token}` },
        });

        if (response.ok) {
            const data = await response.json();
            tableBody.innerHTML = "";
            data.data.users.forEach((user, index) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${user.username}</td>
                    <td>${user.fullname}</td>
                    <td>${user.status}</td>
                    <td>${user.level_name}</td>
                    <td>
                        <button onclick="editUser(${user.id})" class="btn btn-warning">Edit</button>
                        <button onclick="deleteUser(${user.id})" class="btn btn-danger">Hapus</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            alert("Gagal memuat data user.");
        }
    };

    // Fungsi untuk memuat daftar level
    const loadLevels = async () => {
        const response = await fetch(levelEndpoint);
        if (response.ok) {
            const data = await response.json();
            const levelSelect = document.getElementById("level_id");
            levelSelect.innerHTML = "";
            data.data.forEach((level) => {
                const option = document.createElement("option");
                option.value = level.id;
                option.textContent = level.name;
                levelSelect.appendChild(option);
            });
        } else {
            alert("Gagal memuat daftar level.");
        }
    };

    // Fungsi untuk menyimpan user
    userForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const token = localStorage.getItem("jwt_token");
        const formData = new FormData(userForm);
        const userData = Object.fromEntries(formData);

        const method = editId ? "PUT" : "POST";
        const url = editId ? `${apiBase}/${editId}` : apiBase;

        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(userData),
        });

        if (response.ok) {
            alert(editId ? "User berhasil diubah!" : "User berhasil ditambahkan!");
            closeModalFunction();
            loadUsers();
        } else {
            alert("Gagal memproses data user.");
        }
    });

    // Fungsi untuk menghapus user
    window.deleteUser = async (id) => {
        const token = localStorage.getItem("jwt_token");
        if (confirm("Apakah Anda yakin ingin menghapus user ini?")) {
            const response = await fetch(`${apiBase}/${id}`, {
                method: "DELETE",
                headers: { Authorization: `Bearer ${token}` },
            });

            if (response.ok) {
                alert("User berhasil dihapus!");
                loadUsers();
            } else {
                alert("Gagal menghapus user.");
            }
        }
    };

    // Fungsi untuk mengedit user
    window.editUser = async (id) => {
        const token = localStorage.getItem("jwt_token");
        const response = await fetch(`${apiBase}/${id}`, {
            method: "GET",
            headers: { Authorization: `Bearer ${token}` },
        });

        if (response.ok) {
            const data = await response.json();
            openModal(true, data.data.user);
        } else {
            alert("Gagal mengambil data user.");
        }
    };

    // Event listener untuk membuka modal tambah user
    addUserButton.addEventListener("click", () => openModal(false));

    // Event listener untuk menutup modal
    closeModal.addEventListener("click", closeModalFunction);

    // Panggil fungsi loadLevels dan loadUsers saat halaman pertama kali dimuat
    loadLevels();
    loadUsers();
});
