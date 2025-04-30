// Variables globales
let disciplinas = [];
let instructores = [];
let clientes = [];
let chart = null;

// Función para inicializar la página
document.addEventListener('DOMContentLoaded', function() {
    // Cargar datos iniciales
    fetchDisciplinas();
    fetchInstructores();
    fetchClientes();
    
    // Configurar eventos
    setupEventListeners();
    
    // Mostrar notificación de bienvenida
    showNotification('Bienvenido al sistema de gestión de disciplinas', 'info');
});

// Función para configurar los event listeners
function setupEventListeners() {
    // Evento para guardar disciplina
    document.getElementById('saveDisciplina').addEventListener('click', saveDisciplina);
    
    // Evento para aplicar filtros
    document.getElementById('applyFilters').addEventListener('click', applyFilters);
    
    // Evento para cambiar ícono
    document.getElementById('icono').addEventListener('change', updateIconoPreview);
    
    // Evento para buscar en tiempo real
    document.getElementById('searchDisciplina').addEventListener('input', function() {
        if (this.value.length > 2 || this.value.length === 0) {
            applyFilters();
        }
    });
}

// Función para obtener disciplinas
function fetchDisciplinas() {
    // Simulación de datos de API
    disciplinas = [
        { 
            id: 1, 
            nombre: 'Yoga', 
            descripcion: 'Disciplina que busca el equilibrio físico y mental a través de posturas, respiración y meditación.', 
            icono: 'bi-person-arms-up',
            color: '#3498db'
        },
        { 
            id: 2, 
            nombre: 'Pilates', 
            descripcion: 'Sistema de entrenamiento físico y mental que combina diferentes especialidades como gimnasia, traumatología y yoga.', 
            icono: 'bi-heart-pulse',
            color: '#e74c3c'
        },
        { 
            id: 3, 
            nombre: 'Crossfit', 
            descripcion: 'Entrenamiento de alta intensidad que combina ejercicios funcionales, aeróbicos y de fuerza.', 
            icono: 'bi-lightning',
            color: '#2ecc71'
        },
        { 
            id: 4, 
            nombre: 'Spinning', 
            descripcion: 'Ejercicio aeróbico con bicicleta estática que simula un recorrido con diferentes intensidades.', 
            icono: 'bi-bicycle',
            color: '#f39c12'
        },
        { 
            id: 5, 
            nombre: 'Zumba', 
            descripcion: 'Ejercicio aeróbico con ritmos latinos que combina música y baile para mejorar la condición física.', 
            icono: 'bi-music-note-beamed',
            color: '#9b59b6'
        }
    ];
    
    // Renderizar grid de disciplinas
    renderDisciplinasGrid();
    
    // Actualizar estadísticas
    updateStats();
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
}

// Función para obtener clientes
function fetchClientes() {
    // Simulación de datos de API
    clientes = [
        { id: 1, nombres: 'Roberto', apellidos: 'García', celular: 123456789, email: 'roberto@example.com', direccion: 'Calle Principal 123', tipo_cliente: 'interno', status: 1, imagen: 'cliente1.jpg', fecha_pago: '2023-05-15', Discipline_id: 1, instructores: [1, 3] },
        { id: 2, nombres: 'Laura', apellidos: 'Fernández', celular: 987654321, email: 'laura@example.com', direccion: 'Avenida Central 456', tipo_cliente: 'externo', status: 1, imagen: 'cliente2.jpg', fecha_pago: '2023-06-20', Discipline_id: 2, instructores: [2] },
        { id: 3, nombres: 'Miguel', apellidos: 'Torres', celular: 456789123, email: 'miguel@example.com', direccion: 'Plaza Mayor 789', tipo_cliente: 'interno', status: 0, imagen: 'cliente3.jpg', fecha_pago: '2023-04-10', Discipline_id: 3, instructores: [3, 5] },
        { id: 4, nombres: 'Sofía', apellidos: 'Ramírez', celular: 789123456, email: 'sofia@example.com', direccion: 'Calle Secundaria 321', tipo_cliente: 'interno', status: 1, imagen: 'cliente4.jpg', fecha_pago: '2023-07-05', Discipline_id: 4, instructores: [4] },
        { id: 5, nombres: 'Javier', apellidos: 'López', celular: 321654987, email: 'javier@example.com', direccion: 'Avenida Principal 654', tipo_cliente: 'externo', status: 1, imagen: 'cliente5.jpg', fecha_pago: '2023-06-15', Discipline_id: 5, instructores: [1, 2] },
        { id: 6, nombres: 'Carmen', apellidos: 'Díaz', celular: 654987321, email: 'carmen@example.com', direccion: 'Calle Nueva 789', tipo_cliente: 'interno', status: 1, imagen: 'cliente6.jpg', fecha_pago: '2023-07-10', Discipline_id: 1, instructores: [1] },
        { id: 7, nombres: 'Daniel', apellidos: 'Ruiz', celular: 987321654, email: 'daniel@example.com', direccion: 'Avenida Sur 456', tipo_cliente: 'interno', status: 1, imagen: 'cliente7.jpg', fecha_pago: '2023-06-25', Discipline_id: 3, instructores: [3] }
    ];
}

// Función para renderizar el grid de disciplinas
function renderDisciplinasGrid() {
    const disciplinasGrid = document.getElementById('disciplinasGrid');
    disciplinasGrid.innerHTML = '';
    
    if (disciplinas.length === 0) {
        disciplinasGrid.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="bi bi-search" style="font-size: 3rem; color: #ccc;"></i>
                <h4 class="mt-3">No se encontraron disciplinas</h4>
                <p class="text-muted">Intente con otros criterios de búsqueda</p>
            </div>
        `;
        return;
    }
    
    disciplinas.forEach(disciplina => {
        const col = document.createElement('div');
        col.className = 'col-md-6 mb-4 fade-in';
        
        // Contar instructores asignados
        const instructoresCount = instructores.filter(instructor => 
            instructor.Discipline_id === disciplina.id
        ).length;
        
        // Contar clientes asignados
        const clientesCount = clientes.filter(cliente => 
            cliente.Discipline_id === disciplina.id
        ).length;
        
        col.innerHTML = `
            <div class="card disciplina-card">
                <div class="disciplina-header" style="background-color: ${disciplina.color}">
                    <i class="bi ${disciplina.icono} disciplina-icon"></i>
                    <h4>${disciplina.nombre}</h4>
                </div>
                <div class="disciplina-body">
                    <p class="disciplina-description">${disciplina.descripcion}</p>
                    <div class="disciplina-stats">
                        <div class="disciplina-stat">
                            <div class="disciplina-stat-value">${instructoresCount}</div>
                            <div class="disciplina-stat-label">Instructores</div>
                        </div>
                        <div class="disciplina-stat">
                            <div class="disciplina-stat-value">${clientesCount}</div>
                            <div class="disciplina-stat-label">Clientes</div>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between mt-3">
                        <button class="btn btn-sm btn-outline-primary" onclick="viewDisciplina(${disciplina.id})">
                            <i class="bi bi-eye"></i> Ver Detalles
                        </button>
                        <div>
                            <button class="btn btn-sm btn-warning" onclick="editDisciplina(${disciplina.id})">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="deleteDisciplina(${disciplina.id})">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        disciplinasGrid.appendChild(col);
    });
}

// Función para actualizar estadísticas
function updateStats() {
    // Total de disciplinas
    document.getElementById('totalDisciplinas').textContent = disciplinas.length;
    
    // Disciplina más popular (con más clientes)
    const disciplinasConClientes = disciplinas.map(disciplina => {
        const clientesCount = clientes.filter(cliente => cliente.Discipline_id === disciplina.id).length;
        return { ...disciplina, clientesCount };
    });
    
    disciplinasConClientes.sort((a, b) => b.clientesCount - a.clientesCount);
    
    if (disciplinasConClientes.length > 0) {
        document.getElementById('disciplinaPopular').textContent = disciplinasConClientes[0].nombre;
    }
    
    // Gráfico de instructores por disciplina
    renderChart();
}

// Función para renderizar el gráfico
function renderChart() {
    const ctx = document.getElementById('disciplinasChart').getContext('2d');
    
    // Destruir gráfico anterior si existe
    if (chart) {
        chart.destroy();
    }
    
    // Preparar datos para el gráfico
    const labels = disciplinas.map(d => d.nombre);
    const data = disciplinas.map(d => {
        return instructores.filter(i => i.Discipline_id === d.id).length;
    });
    const backgroundColors = disciplinas.map(d => d.color);
    
    // Crear nuevo gráfico
    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Instructores',
                data: data,
                backgroundColor: backgroundColors,
                borderColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Función para aplicar filtros
function applyFilters() {
    const searchTerm = document.getElementById('searchDisciplina').value.toLowerCase();
    const sortOrder = document.querySelector('input[name="sortOrder"]:checked').value;
    
    // Obtener todas las disciplinas originales
    fetchDisciplinas();
    
    // Aplicar filtro de búsqueda
    if (searchTerm) {
        disciplinas = disciplinas.filter(disciplina => 
            disciplina.nombre.toLowerCase().includes(searchTerm) || 
            disciplina.descripcion.toLowerCase().includes(searchTerm)
        );
    }
    
    // Aplicar ordenamiento
    if (sortOrder === 'nombre') {
        disciplinas.sort((a, b) => a.nombre.localeCompare(b.nombre));
    } else if (sortOrder === 'popularidad') {
        disciplinas.sort((a, b) => {
            const clientesA = clientes.filter(cliente => cliente.Discipline_id === a.id).length;
            const clientesB = clientes.filter(cliente => cliente.Discipline_id === b.id).length;
            return clientesB - clientesA;
        });
    }
    
    // Actualizar grid y estadísticas
    renderDisciplinasGrid();
    updateStats();
}

// Función para ver detalles de una disciplina
function viewDisciplina(disciplinaId) {
    const disciplina = disciplinas.find(d => d.id === disciplinaId);
    if (!disciplina) return;
    
    // Llenar modal con datos de la disciplina
    document.getElementById('disciplinaNombre').textContent = disciplina.nombre;
    document.getElementById('disciplinaDescripcion').textContent = disciplina.descripcion;
    
    // Ícono y color
    const iconContainer = document.getElementById('disciplinaIconContainer');
    iconContainer.style.backgroundColor = disciplina.color;
    
    const iconElement = document.getElementById('disciplinaIcono');
    iconElement.className = `bi ${disciplina.icono}`;
    
    // Instructores asignados
    renderDisciplinaInstructores(disciplina);
    
    // Clientes asignados
    renderDisciplinaClientes(disciplina);
    
    // Mostrar el modal
    const viewDisciplinaModal = new bootstrap.Modal(document.getElementById('viewDisciplinaModal'));
    viewDisciplinaModal.show();
}

// Función para mostrar los instructores asignados a la disciplina
function renderDisciplinaInstructores(disciplina) {
    const disciplinaInstructores = document.getElementById('disciplinaInstructores');
    disciplinaInstructores.innerHTML = '';
    
    // Filtrar instructores asignados a esta disciplina
    const instructoresAsignados = instructores.filter(instructor => 
        instructor.Discipline_id === disciplina.id
    );
    
    if (instructoresAsignados.length === 0) {
        disciplinaInstructores.innerHTML = '<div class="col-12 text-center text-muted">No hay instructores asignados</div>';
        return;
    }
    
    instructoresAsignados.forEach(instructor => {
        const col = document.createElement('div');
        col.className = 'col-md-6 mb-3';
        
        col.innerHTML = `
            <div class="d-flex align-items-center">
                <img src="../img/${instructor.imagen}" alt="${instructor.nombres}" class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
                <div>
                    <div class="fw-bold">${instructor.nombres} ${instructor.apellidos}</div>
                    <small class="text-muted">${instructor.email}</small>
                </div>
            </div>
        `;
        
        disciplinaInstructores.appendChild(col);
    });
}

// Función para mostrar los clientes asignados a la disciplina
function renderDisciplinaClientes(disciplina) {
    const disciplinaClientes = document.getElementById('disciplinaClientes');
    disciplinaClientes.innerHTML = '';
    
    // Filtrar clientes asignados a esta disciplina
    const clientesAsignados = clientes.filter(cliente => 
        cliente.Discipline_id === disciplina.id
    );
    
    if (clientesAsignados.length === 0) {
        disciplinaClientes.innerHTML = '<div class="col-12 text-center text-muted">No hay clientes asignados</div>';
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
        
        disciplinaClientes.appendChild(col);
    });
}

// Función para editar una disciplina
function editDisciplina(disciplinaId) {
    const disciplina = disciplinas.find(d => d.id === disciplinaId);
    if (!disciplina) return;
    
    // Llenar formulario con datos de la disciplina
    document.getElementById('disciplinaId').value = disciplina.id;
    document.getElementById('nombre').value = disciplina.nombre;
    document.getElementById('descripcion').value = disciplina.descripcion;
    document.getElementById('icono').value = disciplina.icono;
    document.getElementById('color').value = disciplina.color;
    
    // Actualizar vista previa del ícono
    updateIconoPreview();
    
    // Cambiar título del modal
    document.getElementById('modalTitle').textContent = 'Editar Disciplina';
    
    // Mostrar el modal
    const disciplinaModal = new bootstrap.Modal(document.getElementById('disciplinaModal'));
    disciplinaModal.show();
}

// Función para eliminar una disciplina
function deleteDisciplina(disciplinaId) {
    if (confirm('¿Está seguro de que desea eliminar esta disciplina?')) {
        // Verificar si hay instructores o clientes asignados
        const instructoresAsignados = instructores.filter(instructor => instructor.Discipline_id === disciplinaId).length;
        const clientesAsignados = clientes.filter(cliente => cliente.Discipline_id === disciplinaId).length;
        
        if (instructoresAsignados > 0 || clientesAsignados > 0) {
            if (!confirm(`Esta disciplina tiene ${instructoresAsignados} instructores y ${clientesAsignados} clientes asignados. ¿Desea eliminarla de todas formas?`)) {
                return;
            }
        }
        
        // Filtrar la disciplina a eliminar
        disciplinas = disciplinas.filter(disciplina => disciplina.id !== disciplinaId);
        
        // Actualizar el grid y estadísticas
        renderDisciplinasGrid();
        updateStats();
        
        // Mostrar notificación
        showNotification('Disciplina eliminada correctamente', 'success');
    }
}

// Función para guardar una disciplina (crear o actualizar)
function saveDisciplina() {
    // Obtener datos del formulario
    const disciplinaId = document.getElementById('disciplinaId').value;
    const nombre = document.getElementById('nombre').value;
    const descripcion = document.getElementById('descripcion').value;
    const icono = document.getElementById('icono').value;
    const color = document.getElementById('color').value;
    
    // Validar campos requeridos
    if (!nombre || !descripcion) {
        showNotification('Por favor complete todos los campos requeridos', 'danger');
        return;
    }
    
    // Crear objeto disciplina
    const disciplina = {
        nombre,
        descripcion,
        icono,
        color
    };
    
    // Determinar si es crear o actualizar
    if (disciplinaId) {
        // Actualizar disciplina existente
        disciplina.id = parseInt(disciplinaId);
        const index = disciplinas.findIndex(d => d.id === disciplina.id);
        
        if (index !== -1) {
            // Actualizar disciplina
            disciplinas[index] = disciplina;
            showNotification('Disciplina actualizada correctamente', 'success');
        }
    } else {
        // Crear nueva disciplina
        disciplina.id = disciplinas.length > 0 ? Math.max(...disciplinas.map(d => d.id)) + 1 : 1;
        disciplinas.push(disciplina);
        showNotification('Disciplina creada correctamente', 'success');
    }
    
    // Cerrar modal
    const disciplinaModal = bootstrap.Modal.getInstance(document.getElementById('disciplinaModal'));
    disciplinaModal.hide();
    
    // Limpiar formulario
    document.getElementById('disciplinaForm').reset();
    document.getElementById('disciplinaId').value = '';
    document.getElementById('modalTitle').textContent = 'Nueva Disciplina';
    
    // Actualizar grid y estadísticas
    renderDisciplinasGrid();
    updateStats();
}

// Función para actualizar la vista previa del ícono
function updateIconoPreview() {
    const iconoSelect = document.getElementById('icono');
    const iconoPreview = document.getElementById('iconoPreview');
    
    iconoPreview.className = `bi ${iconoSelect.value}`;
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