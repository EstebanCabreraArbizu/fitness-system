// Variables globales - Inicialización correcta
let clientes = [];
let instructores = [];
let productos = [];
let disciplinas = [];

// Función para inicializar la página
document.addEventListener('DOMContentLoaded', function() {
    // Cargar datos
    fetchData();
});

// Función para cargar todos los datos
function fetchData() {
    // Simulación de carga de datos
    fetchClientes();
    fetchInstructores();
    fetchProductos();
    fetchDisciplinas();
    
    // Actualizar contadores
    updateCounters();
    
    // Cargar últimos clientes
    loadUltimosClientes();
    
    // Cargar productos destacados
    loadProductosDestacados();
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
        },
        {
            id: 4,
            title: 'Pre-Workout Energizante',
            category: 3,
            description: 'Fórmula pre-entrenamiento con cafeína, beta-alanina y citrulina para máxima energía y bombeo muscular.',
            marca: 'ExtremePump',
            purchase_price: 22.00,
            price: 34.99,
            descuento: 0,
            previous_price: 34.99,
            date: '2023-07-05',
            user_id: 4,
            status: 1,
            relevant: 0,
            additional: 'Sabor frutas del bosque',
            outstanding: 1,
            palabras_claves: 'pre-workout, energía, bombeo, entrenamiento',
            fecha_inicio: '2023-04-01',
            fecha_fin: '2023-12-15',
            profesor: 'Ana López',
            profesor_foto: 'instructor4.jpg',
            images: ['producto4_1.jpg'],
            instructores: [4]
        },
        {
            id: 5,
            title: 'Multivitamínico Fitness',
            category: 4,
            description: 'Complejo multivitamínico especialmente formulado para deportistas y personas activas.',
            marca: 'VitaSport',
            purchase_price: 12.50,
            price: 19.99,
            descuento: 2.00,
            previous_price: 21.99,
            date: '2023-03-15',
            user_id: 5,
            status: 1,
            relevant: 1,
            additional: '60 cápsulas',
            outstanding: 0,
            palabras_claves: 'vitaminas, minerales, salud, rendimiento',
            fecha_inicio: '2023-01-15',
            fecha_fin: '2023-11-15',
            profesor: 'Pedro Martínez',
            profesor_foto: 'instructor5.jpg',
            images: ['producto5_1.jpg', 'producto5_2.jpg'],
            instructores: [1, 2, 5]
        },
        {
            id: 6,
            title: 'Barras Proteicas',
            category: 2,
            description: 'Barras con alto contenido proteico y bajo en azúcares para un snack saludable.',
            marca: 'FitSnack',
            purchase_price: 10.00,
            price: 16.99,
            descuento: 1.00,
            previous_price: 17.99,
            date: '2023-02-28',
            user_id: 1,
            status: 0,
            relevant: 0,
            additional: 'Caja de 12 unidades',
            outstanding: 0,
            palabras_claves: 'barras, proteína, snack, saludable',
            fecha_inicio: '2023-02-01',
            fecha_fin: '2023-09-30',
            profesor: 'Juan Pérez',
            profesor_foto: 'instructor1.jpg',
            images: ['producto6_1.jpg'],
            instructores: [1]
        }
    ];
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
}

// Función para actualizar contadores
function updateCounters() {
    // Contar clientes activos
    const clientesActivos = clientes.filter(cliente => cliente.status === 1).length;
    document.getElementById('totalClientes').textContent = clientesActivos;
    
    // Contar instructores activos
    const instructoresActivos = instructores.filter(instructor => instructor.status === 1).length;
    document.getElementById('totalInstructores').textContent = instructoresActivos;
    
    // Contar productos activos
    const productosActivos = productos.filter(producto => producto.status === 1).length;
    document.getElementById('totalProductos').textContent = productosActivos;
    
    // Contar disciplinas
    document.getElementById('totalDisciplinas').textContent = disciplinas.length;
    
    // Animar contadores
    animateCounters();
}

// Función para animar contadores
function animateCounters() {
    const counters = document.querySelectorAll('#totalClientes, #totalInstructores, #totalProductos, #totalDisciplinas');
    
    counters.forEach(counter => {
        counter.classList.add('pulse');
        setTimeout(() => {
            counter.classList.remove('pulse');
        }, 1500);
    });
}

// Función para cargar los últimos clientes
function loadUltimosClientes() {
    const ultimosClientesContainer = document.getElementById('ultimosClientes');
    ultimosClientesContainer.innerHTML = '';
    
    // Ordenar clientes por fecha de pago (más recientes primero)
    const clientesOrdenados = [...clientes]
        .filter(cliente => cliente.fecha_pago) // Solo clientes con fecha de pago
        .sort((a, b) => new Date(b.fecha_pago) - new Date(a.fecha_pago))
        .slice(0, 5); // Tomar los 5 más recientes
    
    if (clientesOrdenados.length === 0) {
        ultimosClientesContainer.innerHTML = `
            <tr>
                <td colspan="5" class="text-center">No hay clientes registrados</td>
            </tr>
        `;
        return;
    }
    
    clientesOrdenados.forEach(cliente => {
        const row = document.createElement('tr');
        row.className = 'fade-in';
        
        // Obtener nombre de la disciplina
        const disciplinaNombre = getDisciplinaNombre(cliente.Discipline_id);
        
        // Formatear fecha
        const fechaPago = cliente.fecha_pago ? new Date(cliente.fecha_pago).toLocaleDateString() : 'No registrado';
        
        // Tipo de cliente
        const tipoBadge = cliente.tipo_cliente === 'interno' 
            ? '<span class="badge bg-primary">Interno</span>' 
            : '<span class="badge bg-warning text-dark">Externo</span>';
        
        row.innerHTML = `
            <td>
                <div class="d-flex align-items-center">
                    <img src="img/${cliente.imagen}" alt="${cliente.nombres}" class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
                    <div>
                        <div class="fw-bold">${cliente.nombres} ${cliente.apellidos}</div>
                        <small class="text-muted">${cliente.email}</small>
                    </div>
                </div>
            </td>
            <td>${tipoBadge}</td>
            <td>${disciplinaNombre}</td>
            <td>${fechaPago}</td>
            <td>
                <a href="clientes/index.html" class="btn btn-sm btn-primary">
                    <i class="bi bi-eye"></i>
                </a>
            </td>
        `;
        
        ultimosClientesContainer.appendChild(row);
    });
}

// Función para cargar productos destacados
function loadProductosDestacados() {
    const productosDestacadosContainer = document.getElementById('productosDestacados');
    productosDestacadosContainer.innerHTML = '';
    
    // Filtrar productos destacados y activos
    const productosDestacados = productos
        .filter(producto => producto.outstanding === 1 && producto.status === 1)
        .slice(0, 3); // Tomar los 3 primeros
    
    if (productosDestacados.length === 0) {
        productosDestacadosContainer.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-search" style="font-size: 2rem; color: #ccc;"></i>
                <p class="mt-2 text-muted">No hay productos destacados</p>
            </div>
        `;
        return;
    }
    
    productosDestacados.forEach(producto => {
        // Obtener imagen principal o imagen por defecto
        const imagenPrincipal = producto.images && producto.images.length > 0 
            ? `img/${producto.images[0]}` 
            : 'img/producto-default.jpg';
        
        // Calcular precio con descuento
        const precioFinal = producto.descuento > 0 
            ? (producto.price - producto.descuento).toFixed(2) 
            : producto.price.toFixed(2);
        
        // Determinar si mostrar precio anterior
        const precioAnteriorHTML = producto.descuento > 0 
            ? `<span class="text-decoration-line-through text-muted ms-2">$${producto.price.toFixed(2)}</span>` 
            : '';
        
        const productoElement = document.createElement('div');
        productoElement.className = 'card mb-3 producto-card';
        productoElement.innerHTML = `
            <div class="row g-0">
                <div class="col-md-4">
                    <img src="${imagenPrincipal}" class="img-fluid rounded-start h-100" alt="${producto.title}" style="object-fit: cover;">
                </div>
                <div class="col-md-8">
                    <div class="card-body">
                        <h5 class="card-title">${producto.title}</h5>
                        <p class="card-text"><small class="text-muted">${producto.marca}</small></p>
                        <div class="d-flex align-items-center mb-2">
                            <span class="fw-bold text-primary">$${precioFinal}</span>
                            ${precioAnteriorHTML}
                        </div>
                        <a href="productos/index.html" class="btn btn-sm btn-outline-primary">Ver Detalles</a>
                    </div>
                </div>
            </div>
        `;
        
        productosDestacadosContainer.appendChild(productoElement);
    });
}

// Función para obtener el nombre de una disciplina por su ID
function getDisciplinaNombre(disciplinaId) {
    const disciplina = disciplinas.find(d => d.id === disciplinaId);
    return disciplina ? disciplina.nombre : 'Desconocida';
}