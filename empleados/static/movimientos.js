document.addEventListener('DOMContentLoaded', function() {
    console.log('Movimientos JS loaded');
    
    const modalMov = document.getElementById('modalInsertarMovimiento');
    const btnAgregarMov = document.getElementById('boton_agregar_movimiento');
    const spanCerrarMov = modalMov.querySelector('.cerrarMov');
    const formMov = document.getElementById('formInsertarMovimiento');


    // Mostrar modal
    btnAgregarMov.addEventListener('click', function() {
        console.log('Botón de agregar movimiento clickeado');
        modalMov.style.display = 'flex';
    });

    // Cerrar modal 
    spanCerrarMov.addEventListener('click', function() {
        modalMov.style.display = 'none';
    });

    // Cerrar al hacer click fuera
    window.addEventListener('click', function(e) {
        if (e.target === modalMov) {
            modalMov.style.display = 'none';
        }
    });

    // Manejar envío del formulario
    formMov.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(this);
        console.log('Sending data:');
        console.log('Identificacion:', formData.get('identificacion'));
        console.log('Tipo movimiento:', formData.get('tipo_movimiento'));
        console.log('Monto:', formData.get('monto'));

        fetch('/home/movimientos/insertar/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.error || 'Error al registrar el movimiento');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de conexión');
        })
        .finally(() => {
            modalMov.style.display = 'none';
        });
    });
});

function validarMonto(input) {
    const valor = parseFloat(input.value);
    const errorSpan = document.getElementById('monto-error');
    
    if (isNaN(valor)) {
        errorSpan.textContent = 'Por favor ingrese un número válido';
        input.setCustomValidity('Número inválido');
        return false;
    }
    
    errorSpan.textContent = '';
    input.setCustomValidity('');
    return true;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            const [key, val] = cookie.trim().split('=');
            if (key === name) cookieValue = decodeURIComponent(val);
        });
    }
    return cookieValue;
}