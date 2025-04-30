// Continuación del archivo clientes.js...

// Función para mostrar los instructores asignados al cliente
function renderClienteInstructores(cliente) {
    const clienteInstructores = document.getElementById('clienteInstructores');
    clienteInstructores.innerHTML = '';
    
    if (!cliente.instructores || cliente.instructores.length === 0) {
        clienteInstructores.innerHTML = '<div class="col-12 text-center text-muted">No hay instructores asignados</div>';
        return;
    }
    
    cliente.instructores.forEach(instructorId => {
        const instructor = instructores.find(i => i.id === instructorId);
        if (!instructor) return;
        
        const col = document.createElement('div');
        col.className = 'col-md-4 mb-3';
        col.innerHTML = `
            <div class="instructor-card">
                <img src="../img/${instructor.imagen}" alt="${instructor.nombres}" class="instructor-img">
                <div class="instructor-name">${instructor.nombres} ${instructor.apellidos}</div>
                <div class="instructor-discipline">${getDisciplinaNombre(instructor.Discipline_id)}</div>
            </div>
        `;
        
        clienteInstructores.appendChild(col);
    });
    
    // Mostrar el modal
    const viewClienteModal = new bootstrap.Modal(document.getElementById('viewClienteModal'));
    viewClienteModal.show();
}

// Función para editar un cliente
function editCliente(clienteId) {
    const cliente = clientes.find(c => c.id === clienteId);
    if (!cliente) return;
    
    // Llenar formulario con datos del cliente
    document.getElementById('clienteId').value = cliente.id;
    document.getElementById('nombres').value = cliente.nombres;
    document.getElementById('apellidos').value = cliente.apellidos;
    document.getElementById('celular').value = cliente.celular;
    document.getElementById('email').value = cliente.email;
    document.getElementById('direccion').value = cliente.direccion;
    document.getElementById('tipo_cliente').value = cliente.tipo_cliente;
    document.getElementById('disciplina').value = cliente.Discipline_id;
    document.getElementById('fecha_pago').value = cliente.fecha_pago || '';
    document.getElementById('status').value = cliente.status;
    
    // Marcar instructores asignados
    const checkboxes = document.querySelectorAll('#instructoresList input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        const instructorId = parseInt(checkbox.value);
        checkbox.checked = cliente.instructores.includes(instructorId);
    });
    
    // Cambiar título del modal
    document.getElementById('modalTitle').textContent = 'Editar Cliente';
    
    // Mostrar el modal
    const clienteModal = new bootstrap.Modal(document.getElementById('clienteModal'));
    clienteModal.show();
}

// Función para eliminar un cliente
function deleteCliente(clienteId) {
    if (confirm('¿Está seguro de que desea eliminar este cliente?')) {
        // Filtrar el cliente a eliminar
        clientes = clientes.filter(cliente => cliente.id !== clienteId);
        
        // Actualizar la tabla
        renderClientesTable();
        
        // Mostrar notificación
        showNotification('Cliente eliminado correctamente', 'success');
    }
}

// Función para guardar un cliente (crear o actualizar)
function saveCliente() {
    // Obtener datos del formulario
    const clienteId = document.getElementById('clienteId').value;
    const nombres = document.getElementById('nombres').value;
    const apellidos = document.getElementById('apellidos').value;
    const celular = document.getElementById('celular').value;
    const email = document.getElementById('email').value;
    const direccion = document.getElementById('direccion').value;
    const tipo_cliente = document.getElementById('tipo_cliente').value;
    const disciplina = parseInt(document.getElementById('disciplina').value);
    const fecha_pago = document.getElementById('fecha_pago').value;
    const status = parseInt(document.getElementById('status').value);
    
    // Validar campos requeridos
    if (!nombres || !apellidos || !celular || !email || !direccion || !tipo_cliente || !disciplina) {
        showNotification('Por favor complete todos los campos requeridos', 'danger');
        return;
    }
    
    // Obtener instructores seleccionados
    const instructoresSeleccionados = [];
    const checkboxes = document.querySelectorAll('#instructoresList input[type="checkbox"]:checked');
    checkboxes.forEach(checkbox => {
        instructoresSeleccionados.push(parseInt(checkbox.value));
    });
    
    // Crear objeto cliente
    const cliente = {
        nombres,
        apellidos,
        celular: parseInt(celular),
        email,
        direccion,
        tipo_cliente,
        Discipline_id: disciplina,
        fecha_pago,
        status,
        imagen: 'default-user.png', // Por defecto, se podría cambiar si se implementa carga de imágenes
        instructores: instructoresSeleccionados
    };
    
    // Determinar si es crear o actualizar
    if (clienteId) {
        // Actualizar cliente existente
        cliente.id = parseInt(clienteId);
        const index = clientes.findIndex(c => c.id === cliente.id);
        
        if (index !== -1) {
            // Mantener la imagen actual si no se seleccionó una nueva
            cliente.imagen = clientes[index].imagen;
            
            // Actualizar cliente
            clientes[index] = cliente;
            showNotification('Cliente actualizado correctamente', 'success');
        }
    } else {
        // Crear nuevo cliente
        cliente.id = clientes.length > 0 ? Math.max(...clientes.map(c => c.id)) + 1 : 1;
        clientes.push(cliente);
        showNotification('Cliente creado correctamente', 'success');
    }
    
    // Cerrar modal
    const clienteModal = bootstrap.Modal.getInstance(document.getElementById('clienteModal'));
    clienteModal.hide();
    
    // Limpiar formulario
    document.getElementById('clienteForm').reset();
    document.getElementById('clienteId').value = '';
    document.getElementById('modalTitle').textContent = 'Nuevo Cliente';
    
    // Actualizar tabla
    renderClientesTable();
}

// Función para previsualizar imagen
function previewImage(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validar que sea una imagen
    if (!file.type.match('image.*')) {
        showNotification('Por favor seleccione un archivo de imagen válido', 'danger');
        event.target.value = '';
        return;
    }
    
    // Simular carga de imagen (en un entorno real, se subiría al servidor)
    showNotification('Imagen seleccionada correctamente', 'info');
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Agregar al DOM
    document.body.appendChild(notification);
    
    // Eliminar después de 5 segundos
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Función para ver cliente
function viewCliente(clienteId) {
    const cliente = clientes.find(c => c.id === clienteId);
    if (!cliente) return;
    
    // Llenar modal con datos del cliente
    document.getElementById('clienteNombreCompleto').textContent = `${cliente.nombres} ${cliente.apellidos}`;
    document.getElementById('clienteEmail').textContent = cliente.email;
    document.getElementById('clienteCelular').textContent = cliente.celular;
    document.getElementById('clienteDireccion').textContent = cliente.direccion;
    document.getElementById('clienteDisciplina').textContent = getDisciplinaNombre(cliente.Discipline_id);
    document.getElementById('clienteFechaPago').textContent = cliente.fecha_pago ? new Date(cliente.fecha_pago).toLocaleDateString() : 'No registrado';
    
    // Imagen del cliente
    document.getElementById('clienteImagen').src = `../img/${cliente.imagen}`;
    
    // Tipo de cliente
    const clienteTipo = document.getElementById('clienteTipo');
    clienteTipo.textContent = cliente.tipo_cliente === 'interno' ? 'Interno (Alumno)' : 'Externo (Temporal)';
    clienteTipo.className = cliente.tipo_cliente === 'interno' ? 'badge bg-primary' : 'badge bg-warning text-dark';
    
    // Estado del cliente
    const clienteStatus = document.getElementById('clienteStatus');
    clienteStatus.textContent = cliente.status === 1 ? 'Activo' : 'Inactivo';
    clienteStatus.className = cliente.status === 1 ? 'badge bg-success' : 'badge bg-danger';
    
    // Instructores asignados
    renderClienteInstructores(cliente);
} 