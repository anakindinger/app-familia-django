document.addEventListener('DOMContentLoaded', function() {
  // Botão de editar rotina
  const editButtons = document.querySelectorAll('[data-edit-rotina]');
  const modal = document.getElementById('modalEditarRotinaUnico');
  if (!modal) return;

  const form = modal.querySelector('form');
  const descInput = form.querySelector('input[name="description"]');
  const startTimeInput = form.querySelector('input[name="start_time"]');
  const endTimeInput = form.querySelector('input[name="end_time"]');
  const startDayInput = form.querySelector('input[name="start_day"]');
  const endDayInput = form.querySelector('input[name="end_day"]');
  const checkboxes = form.querySelectorAll('input[name="days_of_week"]');

  editButtons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      // Pega os dados do botão
      const rotinaId = btn.getAttribute('data-id');
      const desc = btn.getAttribute('data-description');
      const startTime = btn.getAttribute('data-start_time');
      const endTime = btn.getAttribute('data-end_time');
      const startDay = btn.getAttribute('data-start_day');
      const endDay = btn.getAttribute('data-end_day');
      const dias = btn.getAttribute('data-dias'); // Ex: "1,2,3"
      // Preenche os campos
      form.action = `/rotina/alterar/${btn.getAttribute('data-id')}/`;
      descInput.value = desc;
      startTimeInput.value = startTime;
      endTimeInput.value = endTime;
      startDayInput.value = startDay;
      endDayInput.value = endDay || '';
      // Limpa e marca os checkboxes
      checkboxes.forEach(function(chk) {
        chk.checked = dias && dias.split(',').includes(chk.value);
      });
      // Abre o modal
      const bsModal = new bootstrap.Modal(modal);
      bsModal.show();
    });
  });
});
