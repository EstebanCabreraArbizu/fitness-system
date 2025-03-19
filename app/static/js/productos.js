//función para obtener un producto desde el bakckend flask
function fetchProducto(productoId) {
	fetch(URLS.producto(productoId))
		.then(response => {
			if (!response.ok) {
				return response.json().then(err => {
					throw new Error(err.error || 'Error desconocido');
				})
			}
			return response.json();
		})
		.then(producto => {
			//Actualizar la UI con el producto obtenido
			viewProductoData(producto);
		})
		.catch(error => {
			showNotification(error.message || 'Error desconocido', 'danger');
		});
}
// Función auxiliar para cargar los datos en el modal de ver detalles
function viewProductoData(producto) {
	document.getElementById('productoTitle').textContent = producto.title;
	document.getElementById('productoMarca').textContent = producto.marca;
	const productoStatus = document.getElementById('productoStatus');
	productoStatus.textContent = producto.status === 1 ? 'Activo' : 'Inactivo';
	productoStatus.className = producto.status === 1 ? 'badge bg-success' : 'badge bg-danger';

	const precioFinal = producto.descuento > 0
		? (producto.price - producto.descuento).toFixed(2)
		: producto.price.toFixed(2);
	document.getElementById('productoPrecio').textContent = `$${precioFinal}`;

	if (producto.previous_price > producto.price) {
		document.getElementById('productoDescuento').textContent = `$${producto.previous_price.toFixed(2)}`;
		document.getElementById('productoDescuento').style.display = 'inline';
	} else if (producto.descuento > 0) {
		document.getElementById('productoDescuento').textContent = `$${producto.price.toFixed(2)}`;
		document.getElementById('productoDescuento').style.display = 'inline';
	} else {
		document.getElementById('productoDescuento').style.display = 'none';
	}

	document.getElementById('productoDescripcion').textContent = producto.description;
	document.getElementById('productoPalabrasClave').textContent = producto.palabras_claves;
	const fechaInicio = producto.fecha_inicio ? new Date(producto.fecha_inicio).toLocaleDateString() : 'No definida';
	const fechaFin = producto.fecha_fin ? new Date(producto.fecha_fin).toLocaleDateString() : 'No definida';
	document.getElementById('productoFechas').textContent = `${fechaInicio} - ${fechaFin}`;

	// document.getElementById('productoProfesor').textContent = producto.profesor;
	// document.getElementById('productoProfesorFoto').src = `/static/img/${producto.profesor_foto}`;

	// Cargar imágenes del producto
	const productoImagenes = document.getElementById('productoImagenes');
	productoImagenes.innerHTML = '';
	if (producto.images && producto.images.length > 0) {
		producto.images.forEach((imagen, index) => {
			let carouselItem = document.createElement('div');
			carouselItem.className = `carousel-item ${index === 0 ? 'active' : ''}`;
			carouselItem.innerHTML = `
                <img src="/static/img/${imagen}" class="d-block w-100" alt="${producto.title}">
            `;
			productoImagenes.appendChild(carouselItem);
		});
	} else {
		let carouselItem = document.createElement('div');
		carouselItem.className = 'carousel-item active';
		carouselItem.innerHTML = `
            <img src="/static/img/producto-default.png" class="d-block w-100" alt="${producto.title}">
        `;
		productoImagenes.appendChild(carouselItem);
	}

	renderProductoInstructores(producto);
	const viewProductoModal = new bootstrap.Modal(document.getElementById('viewProductoModal'));
	viewProductoModal.show();
}

// Función para guardar (crear/actualizar) producto usando fetch con envío de FormData
// En productos.js
function saveProducto() {
	// Obtener el formulario y crear FormData
	const productoForm = document.getElementById('productoForm');
	const formData = new FormData(productoForm);

	// Verificar si estamos editando o creando
	const productoId = document.getElementById('productoId').value;
	const isEditing = productoId ? true : false;
	// Comprobar que los campos requeridos están completos

	const title = document.getElementById('title').value.trim();
	const marca = document.getElementById('marca').value.trim();
	const palabras_claves = document.getElementById('palabras_claves').value.trim();

	if (!title || !marca || !palabras_claves) {
		showNotification('Todos los campos obligatorios deben estar completos', 'danger');
		return;
	}


	// Agregar los campos uno por uno para asegurarnos que existen
	formData.append('title', title);
	formData.append('category', document.getElementById('category').value || '');
	formData.append('description', document.getElementById('description').value || '');
	formData.append('marca', marca); 0
	formData.append('purchase_price', document.getElementById('purchase_price').value || '0');
	formData.append('price', document.getElementById('price').value || '0');
	formData.append('descuento', document.getElementById('descuento').value || '0');
	formData.append('previous_price', document.getElementById('previous_price').value || '0');
	formData.append('fecha_inicio', document.getElementById('fecha_inicio').value || '');
	formData.append('fecha_fin', document.getElementById('fecha_fin').value || '');
	formData.append('status', document.getElementById('status').value || '1');
	formData.append('palabras_claves', palabras_claves);

	// Checkboxes
	formData.append('relevant', document.getElementById('relevant').checked ? '1' : '0');
	formData.append('outstanding', document.getElementById('outstanding').checked ? '1' : '0');


	const productImagesFiles = document.getElementById('productImages').files;
	for (let i = 0; i < productImagesFiles.length; i++) {
		formData.append('productImages', productImagesFiles[i]);
	}

	// Instructores seleccionados
	const instructoresSeleccionados = document.querySelectorAll('#instructoresList input[type="checkbox"]:checked');
	if (instructoresSeleccionados.length > 0) {
		instructoresSeleccionados.forEach(checkbox => {
			formData.append('instructores[]', checkbox.value);
		});
	} else {
		// Para evitar que instructores[] sea undefined o null
		formData.append('instructores[]', '');
	}

	// Para depuración - mostrar qué datos se están enviando
	console.log('Enviando datos:');
	for (const [key, value] of formData.entries()) {
		console.log(`${key}: ${value}`);
	}
	// Si estamos editando, incluir el ID
	if (isEditing) {
		formData.append('id', productoId);
	}

	// Hacer la petición a la URL adecuada según estemos creando o editando
	const url = isEditing ? URLS.updateProducto(productoId) : URLS.addProducto;
	// Realizar la petición
	fetch(url, {
		method: 'POST',
		body: formData
	})
		.then(response => {
			if (!response.ok) {
				// Intentar obtener el mensaje de error
				return response.json().then(data => {
					throw new Error(data.error || `Error ${response.status}: ${response.statusText}`);
				}).catch(err => {
					// Si no hay JSON, usar el error HTTP genérico
					throw new Error(`Error ${response.status}: ${response.statusText}`);
				});
			}
			return response.json();
		})
		.then(data => {
			console.log('Respuesta:', data);

			if (data.success) {
				showNotification('Producto guardado correctamente', 'success');

				// Cerrar modal y resetear formulario
				const modal = bootstrap.Modal.getInstance(document.getElementById('productoModal'));
				if (modal) modal.hide();
				productoForm.reset();

				// Recargar la página para mostrar el nuevo producto
				setTimeout(() => { window.location.reload(); }, 1500);
			} else {
				showNotification('Error: ' + (data.error || 'Error desconocido'), 'danger');
			}
		})
		.catch(error => {
			console.error('Error en saveProducto:', error);
			showNotification('Error: ' + error.message, 'danger');
		});
}

// Función para mostrar los instructores asignados al producto
function renderProductoInstructores(producto) {
	const productoInstructores = document.getElementById('productoInstructores');
	productoInstructores.innerHTML = '';

	if (!producto.instructores || producto.instructores.length === 0) {
		productoInstructores.innerHTML = '<div class="col-12 text-center text-muted">No hay instructores asignados</div>';
		return;
	}
	console.log('Instructores únicos:', producto.instructores);
	producto.instructores.forEach(instructorId => {
		const instructorIdNum = typeof instructorId === 'string' ? parseInt(instructorId) : instructorId;
		const instructor = instructores.find(i => i.id === instructorIdNum);

		if (!instructor) {
			console.warn(`No se encontró el instructor con ID: ${instructorId}`);
			return;
		}

		const col = document.createElement('div');
		col.className = 'col-md-4 mb-3';
		col.innerHTML = `
            <div class="instructor-card">
                <img src="/static/img/${instructor.imagen}" alt="${instructor.nombres}" class="instructor-img">
                <div class="instructor-name">${instructor.nombres} ${instructor.apellidos}</div>
                <div class="instructor-discipline">${getDisciplinaNombre(instructor.Discipline_id)}</div>
            </div>
        `;

		productoInstructores.appendChild(col);
	});
}

// Función para editar un producto
function editProducto(productoId) {
	fetch(`/products/product/${productoId}`)
		.then(response => {
			if (!response.ok) throw new Error('Producto no encontrado');
			return response.json();
		})
		.then(producto => {
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
                            <img src="/static/img/${imagen}" class="img-thumbnail" alt="${producto.title}">
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
		})
		.catch(error => {
			showNotification(error.message, 'danger');
		});
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
		fetch(URLS.deleteProducto(productoId), {
			method: 'POST'
		})
			.then(response => response.json())
			.then(data => {
				if (data.success) {
					// Eliminar del array local
					const index = productos.findIndex(p => p.id === productoId);
					if (index !== -1) {
						productos.splice(index, 1);
					}

					// Actualizar UI
					renderProductosGrid();
					showNotification('Producto eliminado correctamente', 'success');
				} else {
					showNotification('Error: ' + (data.error || 'No se pudo eliminar'), 'danger');
				}
			})
			.catch(error => {
				console.error('Error:', error);
				showNotification('Error al eliminar el producto', 'danger');
			});
	}
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
		reader.onload = function (e) {
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
// Función para renderizar el grid de productos
function renderProductosGrid() {
	const container = document.getElementById('productosGrid');
	container.innerHTML = '';

	if (!productos || productos.length === 0) {
		container.innerHTML = '<div class="col-12 text-center p-5"><p class="text-muted">No hay productos disponibles</p></div>';
		return;
	}

	const table = document.createElement('table');
	table.className = 'table table-striped table-hover table-bordered table-responsive';

	const thead = document.createElement('thead');
	thead.className = 'table-dark';
	thead.innerHTML = `
		<tr>
            <th scope="col">ID</th>
            <th scope="col">Imagen</th>
            <th scope="col">Título</th>
            <th scope="col">Marca</th>
            <th scope="col">Precio</th>
            <th scope="col">Descuento</th>
            <th scope="col">Precio Final</th>
            <th scope="col">Estado</th>
            <th scope="col">Destacado</th>
            <th scope="col">Relevante</th>
            <th scope="col">Acciones</th>
        </tr>
	`;
	const filterRow = document.createElement('tr');
	filterRow.className = 'filter-row';
	filterRow.innerHTML = `
		<td><input type="text" class="form-control form-control-sm filter" data-column="id" placeholder="ID"></td>
	    <td></td>
	    <td><input type="text" class="form-control form-control-sm filter" data-column="title" placeholder="Título"></td>
	    <td><input type="text" class="form-control form-control-sm filter" data-column="marca" placeholder="Marca"></td>
	    <td><input type="text" class="form-control form-control-sm filter" data-column="price" placeholder="Precio"></td>
	    <td><input type="text" class="form-control form-control-sm filter" data-column="descuento" placeholder="Descuento"></td>
		<td><input type="text" class="form-control form-control-sm filter" data-column="precio final" placeholder="Precio Final"></td>
		<td><input type="text" class="form-control form-control-sm filter" data-column="estado" placeholder="Estado"></td>
		<td><input type="text" class="form-control form-control-sm filter" data-column="destacado" placeholder="Destacado"></td>
		<td><input type="text" class="form-control form-control-sm filter" data-column="relevante" placeholder="Relevante"></td>
		<td><td>
	`;
	thead.appendChild(filterRow);
	table.appendChild(thead);
	const tbody = document.createElement('tbody');

	productos.forEach(producto => {

		// Calcular precio con descuento
		const precioFinal = producto.descuento ? (producto.price - producto.descuento).toFixed(2) : producto.price.toFixed(2);

		// Seleccionar la primera imagen o usar imagen por defecto
		const imagenProducto = producto.images && producto.images.length > 0 ?
			producto.images[0] : 'producto-default.jpg';

		const row = document.createElement('tr');
		row.className = producto.status === 1 ? '' : 'table-secondary';

		row.innerHTML = `
            <td>${producto.id}</td>
            <td class="text-center">
                <img src="/static/img/${imagenProducto}" class="img-thumbnail" 
                    alt="${producto.title}" style="height: 50px; width: 50px; object-fit: cover;">
            </td>
            <td>${producto.title}</td>
            <td>${producto.marca}</td>
            <td class="text-end">${parseFloat(producto.price).toFixed(2)}</td>
            <td class="text-end">${parseFloat(producto.descuento || 0).toFixed(2)}</td>
            <td class="text-end fw-bold">${precioFinal}</td>
            <td class="text-center">
                <span class="badge ${producto.status === 1 ? 'bg-success' : 'bg-secondary'}">
                    ${producto.status === 1 ? 'Activo' : 'Inactivo'}
                </span>
            </td>
            <td class="text-center">
                <i class="bi ${producto.outstanding === 1 ? 'bi-check-circle-fill text-primary' : 'bi-x-circle text-muted'}"></i>
            </td>
            <td class="text-center">
                <i class="bi ${producto.relevant === 1 ? 'bi-check-circle-fill text-success' : 'bi-x-circle text-muted'}"></i>
            </td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="fetchProducto(${producto.id})" title="Ver detalles">
                        <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-outline-secondary" onclick="editProducto(${producto.id})" title="Editar">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-outline-danger" onclick="deleteProducto(${producto.id})" title="Eliminar">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </td>
        `;

		tbody.appendChild(row);
	});
	table.appendChild(tbody);
	const tableResponsive = document.createElement('div');
	tableResponsive.className = 'table-responsive';
	tableResponsive.appendChild(table);
	container.appendChild(tableResponsive);
	document.querySelectorAll('.filter').forEach(input => {
		console.log('Registrando evento input para:', input);
		input.addEventListener('input', applyFilters);
	});
	
}
// Función para aplicar filtros a la tabla de productos
let filterTimeout
function applyFilters() {
	clearTimeout(filterTimeout);
	filterTimeout = setTimeout(() =>{
		console.log('Ejecutando filtros...');
		const filters = {};
		document.querySelectorAll('.filter').forEach(input => {
			const column = input.getAttribute('data-column');
			const value = input.value.trim().toLowerCase();
			if (value) {
				filters[column] = value;
				if (filters[column]) {
					input.classList.add('filter-active');
				} else {
					input.classList.remove('filter-active');
				}
			}
		});
		const filteredProducts = productos.filter(producto => {
			return Object.keys(filters).every(column => {
				if (column === "precio final") {
					const precioFinal = producto.descuento ?
						(producto.price - producto.descuento).toFixed(2) :
						producto.price.toFixed(2);
					return precioFinal.toString().includes(filters[column]);
				}
				else if (column === "estado") {
					const estado = producto.status === 1 ? "activo" : "inactivo";
					return estado.toString().includes(filters[column]);
				}
				else if (column === "destacado") {
					const destacado = producto.outstanding === 1 ? "sí" : "no";
					return destacado.toString().includes(filters[column]);
				}
				else if (column === "relevante") {
					const relevante = producto.relevant === 1 ? "sí" : "no";
					return relevante.toString().includes(filters[column]);
				}
				else {
					// Para todas las demás columnas, buscar normalmente
					// Asegurarse de que el campo exista
					if (producto[column] === undefined) {
						return false;
					}
					// Convertir a string y comparar
					const productValue = String(producto[column]).toLowerCase();
					return productValue.includes(filters[column]);
				}
			});
		});
		renderProductosGridWithData(filteredProducts);
		console.log(`Filtrados ${filteredProducts.length} de ${productos.length} productos.`);
	},300);
}
function clearAllFilters() {
    document.querySelectorAll('.filter').forEach(input => {
        input.value = '';
    });
    applyFilters();
}
function renderProductosGridWithData(data) {
	// Versión de renderProductosGrid() que usa 'data' en lugar de 'productos
	// function renderProductosGrid() {
	const container = document.getElementById('productosGrid');
	container.innerHTML = '';

	if (!data || data.length === 0) {
		container.innerHTML = '<div class="col-12 text-center p-5"><p class="text-muted">No hay productos disponibles</p></div>';
		return;
	}

	const table = document.createElement('table');
	table.className = 'table table-striped table-hover table-bordered table-responsive';

	const thead = document.createElement('thead');
	thead.className = 'table-dark';
	thead.innerHTML = `
		<tr>
            <th scope="col">ID</th>
            <th scope="col">Imagen</th>
            <th scope="col">Título</th>
            <th scope="col">Marca</th>
            <th scope="col">Precio</th>
            <th scope="col">Descuento</th>
            <th scope="col">Precio Final</th>
            <th scope="col">Estado</th>
            <th scope="col">Destacado</th>
            <th scope="col">Relevante</th>
            <th scope="col">Acciones</th>
        </tr>
	`;
	const filterRow = document.createElement('tr');
	filterRow.className = 'filter-row';
	filterRow.innerHTML = `
		<td><input type="text" class="form-control form-control-sm filter" data-column="id" placeholder="ID"></td>
	    <td></td>
	    <td><input type="text" class="form-control form-control-sm filter" data-column="title" placeholder="Título"></td>
	    <td><input type="text" class="form-control form-control-sm filter" data-column="marca" placeholder="Marca"></td>
	    <td><input type="text" class="form-control form-control-sm filter" data-column="price" placeholder="Precio"></td>
	    <td><input type="text" class="form-control form-control-sm filter" data-column="descuento" placeholder="Descuento"></td>
		<td><input type="text" class="form-control form-control-sm filter" data-column="precio final" placeholder="Precio Final"></td>
		<td><input type="text" class="form-control form-control-sm filter" data-column="estado" placeholder="Estado"></td>
		<td><input type="text" class="form-control form-control-sm filter" data-column="destacado" placeholder="Destacado"></td>
		<td><input type="text" class="form-control form-control-sm filter" data-column="relevante" placeholder="Relevante"></td>
		<td><td>
	`;
	thead.appendChild(filterRow);
	table.appendChild(thead);
	const tbody = document.createElement('tbody');
	data.forEach(producto => {

		// Calcular precio con descuento
		const precioFinal = producto.descuento ? (producto.price - producto.descuento).toFixed(2) : producto.price.toFixed(2);

		// Seleccionar la primera imagen o usar imagen por defecto
		const imagenProducto = producto.images && producto.images.length > 0 ?
			producto.images[0] : 'producto-default.jpg';

		const row = document.createElement('tr');
		row.className = producto.status === 1 ? '' : 'table-secondary';

		row.innerHTML = `
            <td>${producto.id}</td>
            <td class="text-center">
                <img src="/static/img/${imagenProducto}" class="img-thumbnail" 
                    alt="${producto.title}" style="height: 50px; width: 50px; object-fit: cover;">
            </td>
            <td>${producto.title}</td>
            <td>${producto.marca}</td>
            <td class="text-end">${parseFloat(producto.price).toFixed(2)}</td>
            <td class="text-end">${parseFloat(producto.descuento || 0).toFixed(2)}</td>
            <td class="text-end fw-bold">${precioFinal}</td>
            <td class="text-center">
                <span class="badge ${producto.status === 1 ? 'bg-success' : 'bg-secondary'}">
                    ${producto.status === 1 ? 'Activo' : 'Inactivo'}
                </span>
            </td>
            <td class="text-center">
                <i class="bi ${producto.outstanding === 1 ? 'bi-check-circle-fill text-primary' : 'bi-x-circle text-muted'}"></i>
            </td>
            <td class="text-center">
                <i class="bi ${producto.relevant === 1 ? 'bi-check-circle-fill text-success' : 'bi-x-circle text-muted'}"></i>
            </td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="fetchProducto(${producto.id})" title="Ver detalles">
                        <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-outline-secondary" onclick="editProducto(${producto.id})" title="Editar">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-outline-danger" onclick="deleteProducto(${producto.id})" title="Eliminar">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </td>
        `;

		tbody.appendChild(row);
	});
	table.appendChild(tbody);
	const tableResponsive = document.createElement('div');
	tableResponsive.className = 'table-responsive';
	tableResponsive.appendChild(table);
	container.appendChild(tableResponsive);
}
// Función para renderizar la lista de instructores en el formulario
function renderInstructoresList() {
	const instructoresList = document.getElementById('instructoresList');
	if (!instructoresList) {
		console.error('No se encontró el elemento con ID "instructoresList"');
		return;
	}
	instructoresList.innerHTML = '';
	if (!instructores || instructores.length === 0) {
		instructoresList.innerHTML = '<div class="col-12 text-center p-3"><p class="text-muted">No hay instructores disponibles</p></div>';
		return;
	}

	instructores.forEach(instructor => {
		const col = document.createElement('div');
		col.className = 'col-md-4 mb-2';
		col.innerHTML = `
            <div class="form-check">
                <input class="form-check-input" type="checkbox" value="${instructor.id}" name="instructores[]" id="instructor${instructor.id}">
                <label class="form-check-label d-flex align-items-center" for="instructor${instructor.id}">
                    <img src="/static/img/${instructor.imagen}" class="rounded-circle me-2" width="30" height="30">
                    ${instructor.nombres} ${instructor.apellidos}
                </label>
            </div>
        `;
		instructoresList.appendChild(col);
	});

	// También actualizar el filtro de instructores
	const filterInstructor = document.getElementById('filterInstructor');
	if (filterInstructor) {
		// Mantener la opción seleccionada actualmente
		const selectedValue = filterInstructor.value;

		// Limpiar opciones actuales excepto la primera
		while (filterInstructor.options.length > 1) {
			filterInstructor.remove(1);
		}

		// Agregar opciones de instructores
		instructores.forEach(instructor => {
			const option = new Option(`${instructor.nombres} ${instructor.apellidos}`, instructor.id);
			filterInstructor.add(option);
		});

		// Restaurar selección
		if (selectedValue) filterInstructor.value = selectedValue;
	}
}
// Función auxiliar para obtener el nombre de una disciplina por ID
function getDisciplinaNombre(disciplineId) {
	// Array de disciplinas (esto podría venir del servidor también)
	const disciplinas = [
		{ id: 1, nombre: "Yoga" },
		{ id: 2, nombre: "Pilates" },
		{ id: 3, nombre: "Crossfit" },
		{ id: 4, nombre: "Spinning" },
		{ id: 5, nombre: "Zumba" }
	];

	const disciplina = disciplinas.find(d => d.id === disciplineId);
	return disciplina ? disciplina.nombre : "No asignada";
}