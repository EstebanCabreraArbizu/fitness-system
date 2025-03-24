/**
 * Clase para manejar el formulario de creación/edición de dietas
 */
export class FormularioDieta {
    /**
     * Constructor
     * @param {DietaService} dietaService - Servicio para manejar dietas
     */
    constructor(dietaService) {
        this.dietaService = dietaService;
        
        // Referencias a elementos DOM
        this.formulario = document.getElementById('dieta-form');
        this.formTitle = document.getElementById('form-title');
        this.dietaId = document.getElementById('dieta-id');
        this.nombreDieta = document.getElementById('nombre-dieta');
        this.objetivoCalorias = document.getElementById('objetivo-calorias');
        this.meta = document.getElementById('meta');
        this.comidasContainer = document.getElementById('comidas-container');
        this.btnAgregarComida = document.getElementById('agregar-comida');
    }
    
    /**
     * Inicializa los eventos del formulario
     */
    init() {
        // Botón para agregar comida
        this.btnAgregarComida.addEventListener('click', () => {
            this.agregarCampoComida();
        });
        
        // Envío del formulario
        this.formulario.addEventListener('submit', (e) => {
            e.preventDefault();
            this.guardarDieta();
        });
    }
    
    /**
     * Carga los datos de una dieta para edición
     * @param {string} dietaId - ID de la dieta a editar
     */
    cargarDieta(dietaId) {
        const dieta = this.dietaService.obtenerDietaPorId(dietaId);
        
        if (!dieta) {
            // Si no se encuentra la dieta, redirigir a la página principal
            window.location.href = 'index.html';
            return;
        }
        
        // Actualizar título y campos
        this.formTitle.textContent = 'Editar Dieta';
        this.dietaId.value = dieta.id;
        this.nombreDieta.value = dieta.nombre;
        this.objetivoCalorias.value = dieta.objetivoCalorias;
        this.meta.value = dieta.meta;
        
        // Cargar comidas
        if (dieta.comidas && dieta.comidas.length > 0) {
            dieta.comidas.forEach(comida => {
                this.agregarCampoComida(comida.nombre, comida.calorias, comida.dia);
            });
        } else {
            // Si no hay comidas, agregar un campo vacío
            this.agregarCampoComida();
        }
    }
    
    /**
     * Agrega un campo para nueva comida al formulario
     * @param {string} [nombre=''] - Nombre de la comida
     * @param {number} [calorias=''] - Calorías de la comida
     * @param {string} [dia='lunes'] - Día de la semana
     */
    agregarCampoComida(nombre = '', calorias = '', dia = 'lunes') {
        const comidaItem = document.createElement('div');
        comidaItem.className = 'comida-item';
        
        const idUnico = 'comida-' + Date.now() + Math.floor(Math.random() * 1000);
        
        comidaItem.innerHTML = `
            <div class="form-row">
                <div class="form-group">
                    <label for="${idUnico}-dia">Día</label>
                    <select id="${idUnico}-dia" name="dia" required>
                        <option value="lunes" ${dia === 'lunes' ? 'selected' : ''}>Lunes</option>
                        <option value="martes" ${dia === 'martes' ? 'selected' : ''}>Martes</option>
                        <option value="miercoles" ${dia === 'miercoles' ? 'selected' : ''}>Miércoles</option>
                        <option value="jueves" ${dia === 'jueves' ? 'selected' : ''}>Jueves</option>
                        <option value="viernes" ${dia === 'viernes' ? 'selected' : ''}>Viernes</option>
                        <option value="sabado" ${dia === 'sabado' ? 'selected' : ''}>Sábado</option>
                        <option value="domingo" ${dia === 'domingo' ? 'selected' : ''}>Domingo</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="${idUnico}-nombre">Nombre de la Comida</label>
                    <input type="text" id="${idUnico}-nombre" name="nombre" value="${nombre}" placeholder="Ej: Ensalada de pollo" required>
                </div>
                
                <div class="form-group">
                    <label for="${idUnico}-calorias">Calorías</label>
                    <input type="number" id="${idUnico}-calorias" name="calorias" value="${calorias}" min="0" placeholder="Ej: 350" required>
                </div>
            </div>
            <button type="button" class="eliminar-comida" aria-label="Eliminar comida"><i class="fas fa-times"></i></button>
        `;
        
        // Agregar evento para eliminar comida
        comidaItem.querySelector('.eliminar-comida').addEventListener('click', () => {
            comidaItem.remove();
        });
        
        this.comidasContainer.appendChild(comidaItem);
    }
    
    /**
     * Guarda los datos de la dieta
     */
    guardarDieta() {
        // Recopilar datos del formulario
        const id = this.dietaId.value;
        const nombre = this.nombreDieta.value;
        const objetivoCalorias = parseInt(this.objetivoCalorias.value);
        const meta = this.meta.value;
        
        // Recopilar comidas
        const comidas = [];
        const comidasItems = this.comidasContainer.querySelectorAll('.comida-item');
        
        comidasItems.forEach(item => {
            const diaSelect = item.querySelector('select[name="dia"]');
            const nombreInput = item.querySelector('input[name="nombre"]');
            const caloriasInput = item.querySelector('input[name="calorias"]');
            
            if (nombreInput.value.trim() !== '') {
                comidas.push({
                    dia: diaSelect.value,
                    nombre: nombreInput.value,
                    calorias: parseInt(caloriasInput.value) || 0
                });
            }
        });
        
        // Crear objeto dieta
        const dieta = {
            id,
            nombre,
            objetivoCalorias,
            meta,
            comidas
        };
        
        // Guardar dieta y redirigir
        this.dietaService.guardarDieta(dieta);
        window.location.href = 'index.html';
    }
} 