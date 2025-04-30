// Variables globales
let instructores = [];
let disciplinas = [];
let productos = [];
let clientes = [];
let currentPage = 1;
const itemsPerPage = 8; // Para mostrar en grid

// Función para inicializar la página
document.addEventListener('DOMContentLoaded', function() {
    // Cargar datos iniciales
    fetchDisciplinas();
    fetchProductos();
    fetchClientes();
    fetchInstructores();
    
    // Configurar eventos
    setupEventListeners();
    
    // Mostrar notificación de bienvenida
    showNotification('Bienvenido al sistema de gestión de instructores', 'info');
});

// Función para configurar los event listeners
function setupEventListeners() {
    // Evento para guardar instructor
    document.getElementById('saveInstructor').addEventListener('click', saveInstructor);
    
    // Eventos para filtros
    document.getElementById('searchInstructor').addEventListener('input', filterInstructores);
    document.getElementById('filterDisciplina').addEventListener('change', filterInstructores);
    document.getElementById('filterStatus').addEventListener('change', filterInstructores);
    
    // Evento para cambiar imagen
    document.getElementById('imagen').addEventListener('change', previewImage);
}

// Función para obtener disciplinas
function fetchDisciplinas() {
    // Simulación de datos de API
    disciplinas = [
        { id: 1, nombre: 'Yoga', descripcion: 'Disciplina que busca el equilibrio físico y mental' },
        { id: 2, nombre: 'Pilates', descripcion: 'Sistema de entrenamiento físico y mental' },
        { id: 3, nombre: 'Crossfit', descripcion: 'Entrenamiento de alta intensidad' },
        { id: 4, nombre: 'Spinning', descripcion: 'Ejercicio aeróbico con bicicleta estática' },
        { id: 5, nombre: 'Zumba', descripcion: 'Ejercicio aeróbico con ritmos latinos' }
    ];
    
    // Llenar select de disciplinas
    const disciplinaSelect = document.getElementById('disciplina');
    const filterDisciplina = document.getElementById('filterDisciplina');
    
    disciplinas.forEach(disciplina => {
        // Para el formulario
        const option = document.createElement('option');
        option.value = disciplina.id;
        option.textContent = disciplina.nombre;
        disciplinaSelect.appendChild(option);
        
        // Para el filtro
        const filterOption = option.cloneNode(true);
        filterDisciplina.appendChild(filterOption);
    });
}

// Función para obtener productos
function fetchProductos() {
    // Simulación de datos de API
    productos = [
        {
            id: 1,
            title: 'Proteína Whey Premium',
            category: 1,
            description: 'Proteína de suero de leche de alta calidad para recuperación muscular.',
            marca: 'FitPower',
            purchase_price: 25.50,
            price: 39.99,
            descuento: 5.00,
            previous_price: 44.99,
            date: '2023-05-10',
            user_id: 1,
            status: 1,
            relevant: 1,
            additional: 'Sin azúcar añadido',
            outstanding: 1,
            palabras_claves: 'proteína, whey, muscular, recuperación',
            fecha_inicio: '2023-01-01',
            fecha_fin: '2023-12-31',
            profesor: 'Juan Pérez',
            profesor_foto: 'instructor1.jpg',
            images: ['producto1_1.jpg', 'producto1_2.jpg'],
            instructores: [1, 3]
        },
        {
            id: 2,
            title: 'BCAA Aminoácidos Esenciales',
            category: 1,
            description: 'Aminoácidos de cadena ramificada para mejorar la recuperación y prevenir el catabolismo muscular.',
            marca: 'NutriSport',
            purchase_price: 18.75,
            price: 29.99,
            descuento: 0,
            previous_price: 29.99,
            date: '2023-06-15',
            user_id: 2,
            status: 1,
            relevant: 0,
            additional: 'Sabor limón',
            outstanding: 1,
            palabras_claves: 'bcaa, aminoácidos, recuperación, muscular',
            fecha_inicio: '2023-02-01',
            fecha_fin: '2023-11-30',
            profesor: 'María González',
            profesor_foto: 'instructor2.jpg',
            images: ['producto2_1.jpg'],
            instructores: [2]
        },
        {
            id: 3,
            title: 'Creatina Monohidrato',
            category: 2,
            description: 'Suplemento para aumentar la fuerza y el rendimiento en entrenamientos de alta intensidad.',
            marca: 'PowerFit',
            purchase_price: 15.25,
            price: 24.99,
            descuento: 3.00,
            previous_price: 27.99,
            date: '2023-04-20',
            user_id: 3,
            status: 1,
            relevant: 1,
            additional: 'Micronizada para mejor absorción',
            outstanding: 1,
            palabras_claves: 'creatina, fuerza, rendimiento, energía',
            fecha_inicio: '2023-03-01',
            fecha_fin: '2023-10-31',
            profesor: 'Carlos Rodríguez',
            profesor_foto: 'instructor3.jpg',
            images: ['producto3_1.jpg', 'producto3_2.jpg', 'producto3_3.jpg'],
            instructores: [3, 5]
        }
    ];
    
    // Llenar lista de productos en el formulario
    renderProductosList();
}

// Función para renderizar la lista de productos en el formulario
function renderProductosList() {
    const productosInstructorList = document.getElementById('productosInstructorList');
    if (!productosInstructorList) return;
    
    productosInstructorList.innerHTML = '';
    
    productos.forEach(producto => {
        const col = document.createElement('div');
        col.className = 'col-md-6 mb-2';
        
        const checkboxId = `producto_${producto.id}`;
        
        col.innerHTML = `
            <div class="form-check">
                <input class="form-check-input" type="checkbox" id="${checkboxId}" value="${producto.id}">
                <label class="form-check-label" for="${checkboxId}">
                    ${producto.title} <small class="text-muted">(${producto.marca})</small>
                </label>
            </div>
        `;
        
        productosInstructorList.appendChild(col);
    });
}

// Función para obtener clientes
function fetchClientes() {
    // Simulación de datos de API
    clientes = [
        { id: 1, nombres: 'Roberto', apellidos: 'García', celular: 123456789, email: 'roberto@example.com', direccion: 'Calle Principal 123', tipo_cliente: 'interno', status: 1, imagen: 'cliente1.jpg', fecha_pago: '2023-05-15', Discipline_id: 1, instructores: [1, 3] },
        { id: 2, nombres: 'Laura', apellidos: 'Fernández', celular: 987654321, email: 'laura@example.com', direccion: 'Avenida Central 456', tipo_cliente: 'externo', status: 1, imagen: 'cliente2.jpg', fecha_pago: '2023-06-20', Discipline_id: 2, instructores: [2] },
        { id: 3, nombres: 'Miguel', apellidos: 'Torres', celular: 456789123, email: 'miguel@example.com', direccion: 'Plaza Mayor 789', tipo_cliente: 'interno', status: 0, imagen: 'cliente3.jpg', fecha_pago: '2023-04-10', Discipline_id: 3, instructores: [3, 5] },
        { id: 4, nombres: 'Sofía', apellidos: 'Ramírez', celular: 789123456, email: 'sofia@example.com', direccion: 'Calle Secundaria 321', tipo_cliente: 'interno', status: 1, imagen: 'cliente4.jpg', fecha_pago: '2023-07-05', Discipline_id: 4, instructores: [4] },
        { id: 5, nombres: 'Javier', apellidos: 'López', celular: 321654987, email: 'javier@example.com', direccion: 'Avenida Principal 654', tipo_cliente: 'externo', status: 1, imagen: 'cliente5.jpg', fecha_pago: '2023-06-15', Discipline_id: 5, instructores: [1, 2] }
    ];
}

// Función para obtener instructores
function fetchInstructores() {
    // Simulación de datos de API
    instructores = [
        { id: 1, nombres: 'Juan', apellidos: 'Pérez', celular: 123456789, email: 'juan@example.com', status: 1, imagen: 'instructor1.jpg', Discipline_id: 1 },
        { id: 2, nombres: 'María', apellidos: 'González', celular: 987654321, email: 'maria@example.com', status: 1, imagen: 'instructor2.jpg', Discipline_id: 2 },
        { id: 3, nombres: 'Carlos', apellidos: 'Rodríguez', celular: 456789123, email: 'carlos@example.com', status: 1, imagen: 'instructor3.jpg', Discipline_id: 3 },
        { id: 4, nombres: 'Ana', apellidos: 'López', celular: 789123456, email: 'ana@example.com', status: 1, imagen: 'instructor4.jpg', Discipline_id: 4 },
        { id: 5, nombres: 'Pedro', apellidos: 'Martínez', celular: 321654987, email: 'pedro@example.com', status: 1, imagen: 'instructor5.jpg', Discipline_id: 5 }
    ];
    
    // Renderizar grid de instructores
    renderInstructoresGrid();
}

// Función para renderizar el grid de instructores
function renderInstructoresGrid() {
    const instructoresGrid = document.getElementById('instructoresGrid');
    instructoresGrid.innerHTML = '';
    
    // Aplicar paginación
    const startIndex = (currentPage - 1) * itemsPerPage;
    const paginatedInstructores = instructores.slice(startIndex, startIndex + itemsPerPage);
    
    if (paginatedInstructores.length === 0) {
        instructoresGrid.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="bi bi-search" style="font-size: 3rem; color: #ccc;"></i>
                <h4 class="mt-3">No se encontraron instructores</h4>
                <p class="text-muted">Intente con otros criterios de búsqueda</p>
            </div>
        `;
        return;
    }
    
    paginatedInstructores.forEach(instructor => {
        const col = document.createElement('div');
        col.className = 'col-md-3 mb-4 fade-in';
        
        // Obtener nombre de la disciplina
        const disciplinaNombre = getDisciplinaNombre(instructor.Discipline_id);
        
        // Estado del instructor
        const statusBadge = instructor.status === 1 
            ? '<span class="badge bg-success position-absolute top-0 end-0 m-2">Activo</span>' 
            : '<span class="badge bg-danger position-absolute top-0 end-0 m-2">Inactivo</span>';
        
        // Contar clientes asignados
        const clientesCount = clientes.filter(cliente => 
            cliente.instructores && cliente.instructores.includes(instructor.id)
        ).length;
        
        // Contar productos asignados
        const productosCount = productos.filter(producto => 
            producto.instructores && producto.instructores.includes(instructor.id)
        ).length;
        
        col.innerHTML = `
            <div class="card h-100 instructor-card">
                <div class="position-relative">
                    <img src="../img/${instructor.imagen}" class="card-img-top" alt="${instructor.nombres}" style="height: 200px; object-fit: cover;">
                    ${statusBadge}
                    <div class="instructor-overlay"></div>
                </div>
                <div class="card-body text-center">
                    <h5 class="card-title">${instructor.nombres} ${instructor.apellidos}</h5>
                    <p class="card-text badge bg-primary">${disciplinaNombre}</p>
                    <div class="d-flex justify-content-around mt-3">
                        <div class="text-center">
                            <h6>${clientesCount}</h6>
                            <small class="text-muted">Clientes</small>
                        </div>
                        <div class="text-center">
                            <h6>${productosCount}</h6>
                            <small class="text-muted">Productos</small>
                        </div>
                    </div>
                </div>
                <div class="card-footer bg-transparent border-0 d-flex justify-content-center">
                    <button class="btn btn-sm btn-primary me-2" onclick="viewInstructor(${instructor.id})">
                        <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-warning me-2" onclick="editInstructor(${instructor.id})">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteInstructor(${instructor.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        `;
        
        instructoresGrid.appendChild(col);
    });
    
    // Actualizar paginación
    renderPagination();
}

// Función para renderizar la paginación
function renderPagination() {
    const pagination = document.getElementById('instructoresPagination');
    pagination.innerHTML = '';
    
    const totalPages = Math.ceil(instructores.length / itemsPerPage);
    
    // Botón anterior
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
    prevLi.innerHTML = `
        <a class="page-link" href="#" aria-label="Anterior" ${currentPage > 1 ? 'onclick="changePage(' + (currentPage - 1) + '); return false;"' : ''}>
            <span aria-hidden="true">&laquo;</span>
        </a>
    `;
    pagination.appendChild(prevLi);
    
    // Páginas numeradas
    for (let i = 1; i <= totalPages; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${currentPage === i ? 'active' : ''}`;
        li.innerHTML = `
            <a class="page-link" href="#" onclick="changePage(${i}); return false;">${i}</a>
        `;
        pagination.appendChild(li);
    }
    
    // Botón siguiente
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${currentPage === totalPages ? 'disabled' : ''}`;
    nextLi.innerHTML = `
        <a class="page-link" href="#" aria-label="Siguiente" ${currentPage < totalPages ? 'onclick="changePage(' + (currentPage + 1) + '); return false;"' : ''}>
            <span aria-hidden="true">&raquo;</span>
        </a>
    `;
    pagination.appendChild(nextLi);
}

// Función para cambiar de página
function changePage(page) {
    currentPage = page;
    renderInstructoresGrid();
    
    // Scroll al inicio del grid
    document.querySelector('.card').scrollIntoView({ behavior: 'smooth' });
}

// Función para filtrar instructores
function filterInstructores() {
    const searchTerm = document.getElementById('searchInstructor').value.toLowerCase();
    const disciplinaFilter = document.getElementById('filterDisciplina').value;
    const statusFilter = document.getElementById('filterStatus').value;
    
    // Resetear a la primera página al filtrar
    currentPage = 1;
    
    // Obtener todos los instructores originales
    fetchInstructores();
    
    // Aplicar filtros
    const filteredInstructores = instructores.filter(instructor => {
        // Filtro por término de búsqueda
        const matchesSearch = 
            instructor.nombres.toLowerCase().includes(searchTerm) || 
            instructor.apellidos.toLowerCase().includes(searchTerm) || 
            instructor.email.toLowerCase().includes(searchTerm) ||
            `${instructor.nombres} ${instructor.apellidos}`.toLowerCase().includes(searchTerm);
        
        // Filtro por disciplina
        const matchesDisciplina = disciplinaFilter === '' || instructor.Discipline_id === parseInt(disciplinaFilter);
        
        // Filtro por estado
        const matchesStatus = statusFilter === '' || instructor.status === parseInt(statusFilter);
        
        return matchesSearch && matchesDisciplina && matchesStatus;
    });
    
    // Actualizar la lista con los resultados filtrados
    instructores = filteredInstructores;
    renderInstructoresGrid();
}

// Función para ver detalles de un instructor
function viewInstructor(instructorId) {
    const instructor = instructores.find(i => i.id === instructorId);
    if (!instructor) return;
    
    // Llenar modal con datos del instructor
    document.getElementById('instructorNombreCompleto').textContent = `${instructor.nombres} ${instructor.apellidos}`;
    document.getElementById('instructorEmail').textContent = instructor.email;
    document.getElementById('instructorCelular').textContent = instructor.celular;
    
    // Disciplina
    const disciplinaNombre = getDisciplinaNombre(instructor.Discipline_id);
    document.getElementById('instructorDisciplina').textContent = disciplinaNombre;
    
    // Imagen del instructor
    document.getElementById('instructorImagen').src = `../img/${instructor.imagen}`;
    
    // Estado del instructor
    const instructorStatus = document.getElementById('instructorStatus');
    instructorStatus.textContent = instructor.status === 1 ? 'Activo' : 'Inactivo';
    instructorStatus.className = instructor.status === 1 ? 'badge bg-success' : 'badge bg-danger';
    
    // Clientes asignados
    renderInstructorClientes(instructor);
    
    // Productos asignados
    renderInstructorProductos(instructor);
    
    // Mostrar el modal
    const viewInstructorModal = new bootstrap.Modal(document.getElementById('viewInstructorModal'));
    viewInstructorModal.show();
}

// Función para mostrar los clientes asignados al instructor
function renderInstructorClientes(instructor) {
    const instructorClientes = document.getElementById('instructorClientes');
    instructorClientes.innerHTML = '';
    
    // Filtrar clientes asignados a este instructor
    const clientesAsignados = clientes.filter(cliente => 
        cliente.instructores && cliente.instructores.includes(instructor.id)
    );
    
    if (clientesAsignados.length === 0) {
        instructorClientes.innerHTML = '<div class="col-12 text-center text-muted">No hay clientes asignados</div>';
        return;
    }
    
    clientesAsignados.forEach(cliente => {
        const col = document.createElement('div');
        col.className = 'col-md-6 mb-3';
        
        // Tipo de cliente
        const tipoBadge = cliente.tipo_cliente === 'interno' 
            ? '<span class="badge bg-primary">Interno</span>' 
            : '<span class="badge bg-warning text-dark">Externo</span>';
        
        col.innerHTML = `
            <div class="d-flex align-items-center">
                <img src="../img/${cliente.imagen}" alt="${cliente.nombres}" class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
                <div>
                    <div class="fw-bold">${cliente.nombres} ${cliente.apellidos}</div>
                    <div class="d-flex align-items-center">
                        <small class="text-muted me-2">${cliente.email}</small>
                        ${tipoBadge}
                    </div>
                </div>
            </div>
        `;
        
        instructorClientes.appendChild(col);
    });
}

// Función para mostrar los productos asignados al instructor
function renderInstructorProductos(instructor) {
    const instructorProductos = document.getElementById('instructorProductos');
    instructorProductos.innerHTML = '';
    
    // Filtrar productos asignados a este instructor
    const productosAsignados = productos.filter(producto => 
        producto.instructores && producto.instructores.includes(instructor.id)
    );
    
    if (productosAsignados.length === 0) {
        instructorProductos.innerHTML = '<div class="col-12 text-center text-muted">No hay productos asignados</div>';
        return;
    }
    
    productosAsignados.forEach(producto => {
        const col = document.createElement('div');
        col.className = 'col-md-6 mb-3';
        
        // Obtener imagen principal o imagen por defecto
        const imagenPrincipal = producto.images && producto.images.length > 0 
            ? `../img/${producto.images[0]}` 
            : '../img/producto-default.jpg';
        
        col.innerHTML = `
            <div class="d-flex align-items-center">
                <img src="${imagenPrincipal}" alt="${producto.title}" class="rounded me-2" width="40" height="40" style="object-fit: cover;">
                <div>
                    <div class="fw-bold">${producto.title}</div>
                    <small class="text-muted">${producto.marca}</small>
                </div>
            </div>
        `;
        
        instructorProductos.appendChild(col);
    });
}

// Función para editar un instructor
function editInstructor(instructorId) {
    const instructor = instructores.find(i => i.id === instructorId);
    if (!instructor) return;
    
    // Llenar formulario con datos del instructor
    document.getElementById('instructorId').value = instructor.id;
    document.getElementById('nombres').value = instructor.nombres;
    document.getElementById('apellidos').value = instructor.apellidos;
    document.getElementById('celular').value = instructor.celular;
    document.getElementById('email').value = instructor.email;
    document.getElementById('disciplina').value = instructor.Discipline_id;
    document.getElementById('status').value = instructor.status;
    
    // Mostrar imagen actual
    const imagenPreview = document.getElementById('imagenPreview');
    imagenPreview.style.display = 'block';
    imagenPreview.querySelector('img').src = `../img/${instructor.imagen}`;
    
    // Marcar productos asignados
    const checkboxes = document.querySelectorAll('#productosInstructorList input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        const productoId = parseInt(checkbox.value);
        const producto = productos.find(p => p.id === productoId);
        if (producto && producto.instructores) {
            checkbox.checked = producto.instructores.includes(instructor.id);
        } else {
            checkbox.checked = false;
        }
    });
    
    // Cambiar título del modal
    document.getElementById('modalTitle').textContent = 'Editar Instructor';
    
    // Mostrar el modal
    const instructorModal = new bootstrap.Modal(document.getElementById('instructorModal'));
    instructorModal.show();
}

// Función para eliminar un instructor
function deleteInstructor(instructorId) {
    if (confirm('¿Está seguro de que desea eliminar este instructor?')) {
        // Filtrar el instructor a eliminar
        instructores = instructores.filter(instructor => instructor.id !== instructorId);
        
        // Actualizar el grid
        renderInstructoresGrid();
        
        // Mostrar notificación
        showNotification('Instructor eliminado correctamente', 'success');
    }
}

// Función para guardar un instructor (crear o actualizar)
function saveInstructor() {
    // Obtener datos del formulario
    const instructorId = document.getElementById('instructorId').value;
    const nombres = document.getElementById('nombres').value;
    const apellidos = document.getElementById('apellidos').value;
    const celular = document.getElementById('celular').value;
    const email = document.getElementById('email').value;
    const disciplina = parseInt(document.getElementById('disciplina').value);
    const status = parseInt(document.getElementById('status').value);
    
    // Validar campos requeridos
    if (!nombres || !apellidos || !celular || !email || !disciplina) {
        showNotification('Por favor complete todos los campos requeridos', 'danger');
        return;
    }
    
    // Obtener productos seleccionados
    const productosSeleccionados = [];
    const checkboxes = document.querySelectorAll('#productosInstructorList input[type="checkbox"]:checked');
    checkboxes.forEach(checkbox => {
        productosSeleccionados.push(parseInt(checkbox.value));
    });
    
    // Crear objeto instructor
    const instructor = {
        nombres,
        apellidos,
        celular: parseInt(celular),
        email,
        Discipline_id: disciplina,
        status,
        imagen: 'default-user.png' // Por defecto, se podría cambiar si se implementa carga de imágenes
    };
    
    // Determinar si es crear o actualizar
    if (instructorId) {
        // Actualizar instructor existente
        instructor.id = parseInt(instructorId);
        const index = instructores.findIndex(i => i.id === instructor.id);
        
        if (index !== -1) {
            // Mantener la imagen actual si no se seleccionó una nueva
            instructor.imagen = instructores[index].imagen;
            
            // Actualizar instructor
            instructores[index] = instructor;
            
            // Actualizar productos asignados
            actualizarProductosInstructor(instructor.id, productosSeleccionados);
            
            showNotification('Instructor actualizado correctamente', 'success');
        }
    } else {
        // Crear nuevo instructor
        instructor.id = instructores.length > 0 ? Math.max(...instructores.map(i => i.id)) + 1 : 1;
        instructores.push(instructor);
        
        // Asignar productos al nuevo instructor
        actualizarProductosInstructor(instructor.id, productosSeleccionados);
        
        showNotification('Instructor creado correctamente', 'success');
    }
    
    // Cerrar modal
    const instructorModal = bootstrap.Modal.getInstance(document.getElementById('instructorModal'));
    instructorModal.hide();
    
    // Limpiar formulario
    document.getElementById('instructorForm').reset();
    document.getElementById('instructorId').value = '';
    document.getElementById('modalTitle').textContent = 'Nuevo Instructor';
    document.getElementById('imagenPreview').style.display = 'none';
    
    // Actualizar grid
    renderInstructoresGrid();
}

// Función para actualizar los productos asignados a un instructor
function actualizarProductosInstructor(instructorId, productosSeleccionados) {
    productos.forEach(producto => {
        if (!producto.instructores) {
            producto.instructores = [];
        }
        
        // Eliminar el instructor de todos los productos
        producto.instructores = producto.instructores.filter(id => id !== instructorId);
        
        // Agregar el instructor a los productos seleccionados
        if (productosSeleccionados.includes(producto.id)) {
            producto.instructores.push(instructorId);
        }
    });
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
    
    // Mostrar previsualización
    const reader = new FileReader();
    reader.onload = function(e) {
        const imagenPreview = document.getElementById('imagenPreview');
        imagenPreview.style.display = 'block';
        imagenPreview.querySelector('img').src = e.target.result;
    };
    reader.readAsDataURL(file);
    
    // Simular carga de imagen (en un entorno real, se subiría al servidor)
    showNotification('Imagen seleccionada correctamente', 'info');
}

// Función para obtener el nombre de una disciplina por su ID
function getDisciplinaNombre(disciplinaId) {
    const disciplina = disciplinas.find(d => d.id === disciplinaId);
    return disciplina ? disciplina.nombre : 'Desconocida';
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