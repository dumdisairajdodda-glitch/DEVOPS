// EmployeeHub Core JavaScript

document.addEventListener('DOMContentLoaded', function () {
  // Mobile Sidebar Toggle
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('appSidebar');
  const backdrop = document.getElementById('sidebarBackdrop');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('show');
      if (backdrop) backdrop.classList.toggle('show');
    });
  }

  if (backdrop) {
    backdrop.addEventListener('click', function () {
      sidebar.classList.remove('show');
      backdrop.classList.remove('show');
    });
  }

  // Auto-dismiss bootstrap alerts after 5 seconds
  const autoAlerts = document.querySelectorAll('.alert-dismissible');
  autoAlerts.forEach(function (alert) {
    setTimeout(function () {
      try {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      } catch (e) {}
    }, 5000);
  });

  // Delete Confirmation Modal Handler
  const deleteModal = document.getElementById('deleteConfirmModal');
  if (deleteModal) {
    deleteModal.addEventListener('show.bs.modal', function (event) {
      const button = event.relatedTarget;
      const itemName = button.getAttribute('data-item-name') || 'this item';
      const formAction = button.getAttribute('data-form-action');

      const modalItemSpan = deleteModal.querySelector('#deleteItemName');
      const deleteForm = deleteModal.querySelector('#deleteForm');

      if (modalItemSpan) modalItemSpan.textContent = itemName;
      if (deleteForm && formAction) deleteForm.setAttribute('action', formAction);
    });
  }

  // Edit Department Modal Handler
  const editDeptModal = document.getElementById('editDepartmentModal');
  if (editDeptModal) {
    editDeptModal.addEventListener('show.bs.modal', function (event) {
      const button = event.relatedTarget;
      const deptId = button.getAttribute('data-id');
      const deptName = button.getAttribute('data-name');
      const deptCode = button.getAttribute('data-code');
      const deptDesc = button.getAttribute('data-desc');

      const form = editDeptModal.querySelector('#editDeptForm');
      form.setAttribute('action', '/departments/' + deptId + '/edit');

      editDeptModal.querySelector('#editDeptName').value = deptName;
      editDeptModal.querySelector('#editDeptCode').value = deptCode;
      editDeptModal.querySelector('#editDeptDesc').value = deptDesc || '';
    });
  }

  // Password visibility toggle
  const togglePassBtn = document.getElementById('togglePasswordBtn');
  const passInput = document.getElementById('passwordInput');
  if (togglePassBtn && passInput) {
    togglePassBtn.addEventListener('click', function () {
      const type = passInput.getAttribute('type') === 'password' ? 'text' : 'password';
      passInput.setAttribute('type', type);
      const icon = togglePassBtn.querySelector('i');
      if (icon) {
        icon.classList.toggle('bi-eye');
        icon.classList.toggle('bi-eye-slash');
      }
    });
  }
});

// Helper function to fill login credentials quickly
function fillCredentials(identifier, password) {
  const identInput = document.getElementById('identifierInput');
  const passInput = document.getElementById('passwordInput');
  if (identInput && passInput) {
    identInput.value = identifier;
    passInput.value = password;
  }
}
