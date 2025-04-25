document.addEventListener("DOMContentLoaded", function() {

    //Obtener formulario de inicio de sesión
    const form = document.getElementById("login-form");

    //Evento para cuando se envia el formulario
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        //Obtiene y limpia los valores de los campos de usuario y contraseña
        let username = document.getElementById("username").value.trim();
        let password = document.getElementById("password").value.trim();

        // Validar campos vacíos
        if (!username || !password) {
            // Mostrar alerta de error si los campos están vacíos
            Swal.fire({
                title: 'Error',
                text: 'Complete todos los campos',
                icon: 'error',
                timer: 2000
            });
            return;
        }

        //Imprimir en consola los datos que se van a enviar al servidor (Verificacion)
        console.log("Enviando datos:", { username, password });

        // Enviar datos al servidor
        try {
            const response = await fetch("/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json", // Asegurarse de que se está enviando como JSON
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
                },
                body: JSON.stringify({ username, password })  // Asegurarse de que los datos se envíen como JSON
            });

            //Convierte la respuesta del servidor a JSON
            const data = await response.json();

            //Imprimir en consola la respuesta del servidor (Verificacion)
            console.log("Respuesta del servidor:", data);

            //Verifica si la respuesta es exitosa o no
            if (data.success) {
                // Si la respuesta es exitosa, redirigir al usuario a la página de inicio
                window.location.href = data.redirect;
            } 
            //Si el servidor responde que la ip está bloqueada
            else if (data.error === "blocked") {
                Swal.fire({
                    title: 'Bloqueado',
                    text: data.message,
                    icon: 'error',
                    confirmButtonText: 'OK'
                }).then(() => {
                    window.location.reload(); // Recargar la página para mostrar el mensaje de error
                });
            } 
            //En caso de que las credenciales sean incorrectas
            else {
                Swal.fire({
                    title: 'Error',
                    text: data.message || "Error desconocido",
                    icon: 'error',
                    timer: 2000
                });
            }
        } 
        
        //En caso de que no se pueda conectar al servidor
        catch (error) {
            Swal.fire({
                title: 'Error crítico',
                text: 'No se pudo conectar al servidor',
                icon: 'error',
                timer: 3000
            });
        }
    });
});
