// Preenche o modal de edição de evento ao clicar em "Alterar"
document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modalEditarEventoUnico');
  if (!modal) return;
  const form = modal.querySelector('form');
  const descInput = form.querySelector('input[name="description"]');
  const hourInitInput = form.querySelector('input[name="hour_init"]');
  const hourEndInput = form.querySelector('input[name="hour_end"]');
  const dateInput = form.querySelector('input[name="date"]');

  document.body.addEventListener('click', function(e) {
    const btn = e.target.closest('.btnEditarEventoUnico');
    if (!btn) return;
    descInput.value = btn.getAttribute('data-description') || '';
    hourInitInput.value = btn.getAttribute('data-hour-init') || '';
    hourEndInput.value = btn.getAttribute('data-hour-end') || '';
    dateInput.value = btn.getAttribute('data-date') || '';
    form.action = `/agenda/alterar_evento/${btn.getAttribute('data-eventoid')}/`;
  });

  modal.addEventListener('hidden.bs.modal', function() {
    descInput.value = '';
    hourInitInput.value = '';
    hourEndInput.value = '';
    dateInput.value = '';
    form.action = '';
  });
});
