// Función para ver detalles de un producto
function viewProducto(productoId) {
    const producto = productos.find(p => p.id === productoId);
    if (!producto) return;
    
    // Llenar modal con datos del producto
    document.getElementById('productoTitle').textContent = producto.title;
    document.getElementById('productoMarca').textContent = producto.marca;
    
    // Estado del producto
    const productoStatus = document.getElementById('productoStatus');
    productoStatus.textContent = producto.status === 1 ? 'Activo' : 'Inactivo';
    productoStatus.className = producto.status === 1 ? 'badge bg-success' : 'badge bg-danger';
    
    // Precios
    const precioFinal = producto.descuento > 0 
        ? (producto.price - producto.descuento).toFixed(2) 
        : producto.price.toFixed(2);
    
    // Precios (continuación)
    document.getElementById('productoPrecio').textContent = `$${precioFinal}`;

    if (producto.descuento > 0) {
        document.getElementById('productoDescuento').textContent = `$${producto.price.toFixed(2)}`;
        document.getElementById('productoDescuento').style.display = 'inline';
    } else {
        document.getElementById('productoDescuento').style.display = 'none';
    }

    // Descripción
    document.getElementById('productoDescripcion').textContent = producto.description;

    // Palabras clave
    document.getElementById('productoPalabrasClave').textContent = producto.palabras_claves;

    // Fechas
    const fechaInicio = producto.fecha_inicio ? new Date(producto.fecha_inicio).toLocaleDateString() : 'No definida';
    const fechaFin = producto.fecha_fin ? new Date(producto.fecha_fin).toLocaleDateString() : 'No definida';
    document.getElementById('productoFechas').textContent = `${fechaInicio} - ${fechaFin}`;

    // Profesor
    document.getElementById('productoProfesor').textContent = producto.profesor;
    document.getElementById('productoProfesorFoto').src = `../img/${producto.profesor_foto}`;

    // Imágenes del producto
    const productoImagenes = document.getElementById('productoImagenes');
    productoImagenes.innerHTML = '';

    if (producto.images && producto.images.length > 0) {
        producto.images.forEach((imagen, index) => {
            const carouselItem = document.createElement('div');
            carouselItem.className = `carousel-item ${index === 0 ? 'active' : ''}`;
            carouselItem.innerHTML = `
                <img src="../img/${imagen}" class="d-block w-100" alt="${producto.title}">
            `;
            productoImagenes.appendChild(carouselItem);
        });
    } else {
        // Imagen por defecto si no hay imágenes
        const carouselItem = document.createElement('div');
        carouselItem.className = 'carousel-item active';
        carouselItem.innerHTML = `
            <img src="../img/producto-default.jpg" class="d-block w-100" alt="${producto.title}">
        `;
        productoImagenes.appendChild(carouselItem);
    }

    // Instructores asignados
    renderProductoInstructores(producto);

    // Mostrar el modal
    const viewProductoModal = new bootstrap.Modal(document.getElementById('viewProductoModal'));
    viewProductoModal.show();
}

// Función para mostrar los instructores asignados al producto
function renderProductoInstructores(producto) {
    const productoInstructores = document.getElementById('productoInstructores');
    productoInstructores.innerHTML = '';
    
    if (!producto.instructores || producto.instructores.length === 0) {
        productoInstructores.innerHTML = '<div class="col-12 text-center text-muted">No hay instructores asignados</div>';
        return;
    }
    
    producto.instructores.forEach(instructorId => {
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
        
        productoInstructores.appendChild(col);
    });
}

// Función para editar un producto
function editProducto(productoId) {
    const producto = productos.find(p => p.id === productoId);
    if (!producto) return;
    
    // Llenar formulario con datos del producto
    document.getElementById('productoId').value = producto.id;
    document.getElementById('title').value = producto.title;
    document.getElementById('category').value = producto.category || '';
    document.getElementById('description').value = producto.description || '';
    document.getElementById('marca').value = producto.marca;
    document.getElementById('palabras_claves').value = producto.palabras_claves;
    document.getElementById('purchase_price').value = producto.purchase_price || '';
    document.getElementById('price').value = producto.price || '';
    document.getElementById('descuento').value = producto.descuento || '';
    document.getElementById('previous_price').value = producto.previous_price || '';
    document.getElementById('fecha_inicio').value = producto.fecha_inicio || '';
    document.getElementById('fecha_fin').value = producto.fecha_fin || '';
    document.getElementById('status').value = producto.status;
    document.getElementById('profesor').value = producto.profesor;
    
    // Checkboxes
    document.getElementById('relevant').checked = producto.relevant === 1;
    document.getElementById('outstanding').checked = producto.outstanding === 1;
    
    // Marcar instructores asignados
    const checkboxes = document.querySelectorAll('#instructoresList input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        const instructorId = parseInt(checkbox.value);
        checkbox.checked = producto.instructores && producto.instructores.includes(instructorId);
    });
    
    // Previsualizar imágenes existentes
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    imagePreviewContainer.innerHTML = '';
    
    if (producto.images && producto.images.length > 0) {
        producto.images.forEach(imagen => {
            const col = document.createElement('div');
            col.className = 'col-md-3 mb-2';
            col.innerHTML = `
                <div class="position-relative">
                    <img src="../img/${imagen}" class="img-thumbnail" alt="${producto.title}">
                    <button type="button" class="btn btn-sm btn-danger position-absolute top-0 end-0" 
                            onclick="removeImage(this, '${imagen}')">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            `;
            imagePreviewContainer.appendChild(col);
        });
    }
    
    // Cambiar título del modal
    document.getElementById('modalTitle').textContent = 'Editar Producto';
    
    // Mostrar el modal
    const productoModal = new bootstrap.Modal(document.getElementById('productoModal'));
    productoModal.show();
}

// Función para eliminar una imagen de la previsualización
function removeImage(button, imageName) {
    // En un entorno real, aquí se eliminaría la imagen del servidor
    button.closest('.col-md-3').remove();
    
    // Actualizar el array de imágenes del producto (simulado)
    const productoId = document.getElementById('productoId').value;
    if (productoId) {
        const producto = productos.find(p => p.id === parseInt(productoId));
        if (producto && producto.images) {
            producto.images = producto.images.filter(img => img !== imageName);
        }
    }
    
    showNotification('Imagen eliminada correctamente', 'info');
}

// Función para eliminar un producto
function deleteProducto(productoId) {
    if (confirm('¿Está seguro de que desea eliminar este producto?')) {
        // Filtrar el producto a eliminar
        productos = productos.filter(producto => producto.id !== productoId);
        
        // Actualizar el grid
        renderProductosGrid();
        
        // Mostrar notificación
        showNotification('Producto eliminado correctamente', 'success');
    }
}

// Función para guardar un producto (crear o actualizar)
function saveProducto() {
    // Obtener datos del formulario
    const productoId = document.getElementById('productoId').value;
    const title = document.getElementById('title').value;
    const category = document.getElementById('category').value;
    const description = document.getElementById('description').value;
    const marca = document.getElementById('marca').value;
    const palabras_claves = document.getElementById('palabras_claves').value;
    const purchase_price = document.getElementById('purchase_price').value;
    const price = document.getElementById('price').value;
    const descuento = document.getElementById('descuento').value;
    const previous_price = document.getElementById('previous_price').value;
    const fecha_inicio = document.getElementById('fecha_inicio').value;
    const fecha_fin = document.getElementById('fecha_fin').value;
    const status = parseInt(document.getElementById('status').value);
    const profesor = document.getElementById('profesor').value;
    const relevant = document.getElementById('relevant').checked ? 1 : 0;
    const outstanding = document.getElementById('outstanding').checked ? 1 : 0;
    
    // Validar campos requeridos
    if (!title || !marca || !palabras_claves || !profesor) {
        showNotification('Por favor complete todos los campos requeridos', 'danger');
        return;
    }
    
    // Obtener instructores seleccionados
    const instructoresSeleccionados = [];
    const checkboxes = document.querySelectorAll('#instructoresList input[type="checkbox"]:checked');
    checkboxes.forEach(checkbox => {
        instructoresSeleccionados.push(parseInt(checkbox.value));
    });
    
    // Crear objeto producto
    const producto = {
        title,
        category: category ? parseInt(category) : null,
        description,
        marca,
        palabras_claves,
        purchase_price: purchase_price ? parseFloat(purchase_price) : null,
        price: price ? parseFloat(price) : null,
        descuento: descuento ? parseFloat(descuento) : 0,
        previous_price: previous_price ? parseFloat(previous_price) : null,
        fecha_inicio,
        fecha_fin,
        status,
        profesor,
        profesor_foto: 'default-user.png', // Por defecto, se podría cambiar si se implementa carga de imágenes
        relevant,
        outstanding,
        date: new Date().toISOString().split('T')[0], // Fecha actual
        user_id: 1, // Usuario actual (simulado)
        instructores: instructoresSeleccionados,
        images: [] // Se inicializa vacío y se mantienen las imágenes existentes si es una edición
    };
    
    // Determinar si es crear o actualizar
    if (productoId) {
        // Actualizar producto existente
        producto.id = parseInt(productoId);
        const index = productos.findIndex(p => p.id === producto.id);
        
        if (index !== -1) {
            // Mantener las imágenes actuales si no se seleccionaron nuevas
            producto.images = productos[index].images || [];
            producto.profesor_foto = productos[index].profesor_foto;
            
            // Actualizar producto
            productos[index] = producto;
            showNotification('Producto actualizado correctamente', 'success');
        }
    } else {
        // Crear nuevo producto
        producto.id = productos.length > 0 ? Math.max(...productos.map(p => p.id)) + 1 : 1;
        productos.push(producto);
        showNotification('Producto creado correctamente', 'success');
    }
    
    // Cerrar modal
    const productoModal = bootstrap.Modal.getInstance(document.getElementById('productoModal'));
    productoModal.hide();
    
    // Limpiar formulario
    document.getElementById('productoForm').reset();
    document.getElementById('productoId').value = '';
    document.getElementById('modalTitle').textContent = 'Nuevo Producto';
    document.getElementById('imagePreviewContainer').innerHTML = '';
    
    // Actualizar grid
    renderProductosGrid();
}

// Función para previsualizar imágenes del producto
function previewProductImages(event) {
    const files = event.target.files;
    if (!files || files.length === 0) return;
    
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    
    // Validar que sean imágenes
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        
        if (!file.type.match('image.*')) {
            showNotification('Por favor seleccione solo archivos de imagen válidos', 'danger');
            event.target.value = '';
            return;
        }
        
        // Crear previsualización
        const reader = new FileReader();
        reader.onload = function(e) {
            const col = document.createElement('div');
            col.className = 'col-md-3 mb-2';
            col.innerHTML = `
                <div class="position-relative">
                    <img src="${e.target.result}" class="img-thumbnail" alt="Vista previa">
                    <button type="button" class="btn btn-sm btn-danger position-absolute top-0 end-0" 
                            onclick="this.closest('.col-md-3').remove()">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            `;
            imagePreviewContainer.appendChild(col);
        };
        reader.readAsDataURL(file);
    }
    
    // Simular carga de imágenes (en un entorno real, se subirían al servidor)
    showNotification(`${files.length} imágenes seleccionadas correctamente`, 'info');
}

// Función para previsualizar foto del profesor
function previewProfesorFoto(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validar que sea una imagen
    if (!file.type.match('image.*')) {
        showNotification('Por favor seleccione un archivo de imagen válido', 'danger');
        event.target.value = '';
        return;
    }
    
    // Simular carga de imagen (en un entorno real, se subiría al servidor)
    showNotification('Imagen del profesor seleccionada correctamente', 'info');
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