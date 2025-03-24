/**
 * Clase que maneja la interfaz de usuario y la interacción
 */
export class UI {
    /**
     * Constructor de la clase UI
     * @param {DietaService} dietaService - Servicio para manejar las dietas
     */
    constructor(dietaService) {
        this.dietaService = dietaService;
        
        // Referencias a elementos DOM
        this.listaDietas = document.getElementById('lista-dietas');
        this.totalCalorias = document.getElementById('total-calorias');
        this.totalComidas = document.getElementById('total-comidas');
        this.progresoMeta = document.getElementById('progreso-meta');
        
        // Modal de detalles
        this.detallesModal = document.getElementById('detalles-modal');
        this.detallesTitle = document.getElementById('detalles-title');
        this.detallesContent = document.getElementById('detalles-content');
        
        // Botones
        this.btnCerrarDetalles = document.getElementById('cerrar-detalles');
    }
    
    /**
     * Inicializa los eventos de la interfaz
     */
    init() {
        // Cerrar modal con el botón X
        document.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', () => {
                this.detallesModal.style.display = 'none';
            });
        });
        
        // Botón cerrar en detalles
        this.btnCerrarDetalles.addEventListener('click', () => {
            this.detallesModal.style.display = 'none';
        });
        
        // Cerrar modal al hacer clic fuera
        window.addEventListener('click', (e) => {
            if (e.target === this.detallesModal) {
                this.detallesModal.style.display = 'none';
            }
        });
    }
    
    /**
     * Carga y muestra las dietas almacenadas
     */
    cargarDietas() {
        const dietas = this.dietaService.obtenerDietas();
        
        // Mostrar mensaje si no hay dietas
        if (dietas.length === 0) {
            this.listaDietas.innerHTML = `
                <p class="empty-state">No hay dietas registradas. ¡Crea una nueva dieta para comenzar!</p>
            `;
            return;
        }
        
        // Limpiar contenedor
        this.listaDietas.innerHTML = '';
        
        // Crear y agregar tarjetas de dietas
        dietas.forEach(dieta => {
            this.agregarTarjetaDieta(dieta);
        });
    }
    
    /**
     * Agrega una tarjeta de dieta al listado
     * @param {Object} dieta - Datos de la dieta
     */
    agregarTarjetaDieta(dieta) {
        const totalComidasDieta = dieta.comidas?.length || 0;
        const fechaFormateada = new Date(dieta.fechaCreacion).toLocaleDateString();
        const porcentajeProgreso = Math.min(Math.round((totalComidasDieta / 7) * 100), 100); // Asumimos 7 comidas por semana ideal
        
        const dietaCard = document.createElement('div');
        dietaCard.className = 'dieta-card';
        dietaCard.innerHTML = `
            <div class="dieta-header">
                <div>
                    <h3 class="dieta-title">${dieta.nombre}</h3>
                    <p class="dieta-meta">Creada: ${fechaFormateada}</p>
                </div>
            </div>
            <div class="dieta-stats">
                <span>${dieta.objetivoCalorias} calorías</span>
                <span>${totalComidasDieta} comidas</span>
            </div>
            <div class="progress-bar">
                <div class="progress-bar-fill" style="width: ${porcentajeProgreso}%"></div>
            </div>
            <p><strong>Meta:</strong> ${dieta.meta}</p>
            <div class="dieta-actions">
                <button class="btn ver-dieta" title="Ver detalles" data-id="${dieta.id}"><i class="fas fa-eye"></i></button>
                <a href="crear-dieta.html?id=${dieta.id}" class="btn secondary" title="Editar dieta"><i class="fas fa-edit"></i></a>
                <button class="btn danger eliminar-dieta" title="Eliminar dieta" data-id="${dieta.id}"><i class="fas fa-trash"></i></button>
            </div>
        `;
        
        // Agregar eventos a los botones
        dietaCard.querySelector('.ver-dieta').addEventListener('click', () => {
            this.mostrarDetallesDieta(dieta.id);
        });
        
        dietaCard.querySelector('.eliminar-dieta').addEventListener('click', () => {
            this.eliminarDieta(dieta.id);
        });
        
        this.listaDietas.appendChild(dietaCard);
    }
    
    /**
     * Actualiza el resumen con las estadísticas actuales
     */
    actualizarResumen() {
        const estadisticas = this.dietaService.obtenerEstadisticas();
        
        this.totalCalorias.textContent = estadisticas.totalCalorias.toLocaleString();
        this.totalComidas.textContent = estadisticas.totalComidas;
        this.progresoMeta.textContent = `${estadisticas.progresoMeta}%`;
    }
    
    /**
     * Muestra los detalles de una dieta
     * @param {string} id - ID de la dieta
     */
    mostrarDetallesDieta(id) {
        const dieta = this.dietaService.obtenerDietaPorId(id);
        if (!dieta) return;
        
        this.detallesTitle.textContent = dieta.nombre;
        
        // Crear contenido de detalles
        let contenidoHTML = `
            <div class="detalles-info">
                <p><strong>Objetivo de Calorías:</strong> ${dieta.objetivoCalorias}</p>
                <p><strong>Meta:</strong> ${dieta.meta}</p>
                <p><strong>Fecha de Creación:</strong> ${new Date(dieta.fechaCreacion).toLocaleDateString()}</p>
                ${dieta.fechaModificacion ? `<p><strong>Última Modificación:</strong> ${new Date(dieta.fechaModificacion).toLocaleDateString()}</p>` : ''}
            </div>
            <h4>Comidas Programadas</h4>
        `;
        
        // Si no hay comidas
        if (!dieta.comidas || dieta.comidas.length === 0) {
            contenidoHTML += `<p class="empty-state">No hay comidas registradas para esta dieta.</p>`;
        } else {
            // Agrupar comidas por día
            const comidasPorDia = this.agruparComidasPorDia(dieta.comidas);
            
            contenidoHTML += `<div class="comidas-detalles">`;
            
            // Orden de los días
            const diasOrden = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
            
            // Mostrar comidas agrupadas por día
            diasOrden.forEach(dia => {
                if (comidasPorDia[dia]) {
                    contenidoHTML += `
                        <div class="dia-comidas">
                            <h5>${this.capitalizarPrimeraLetra(dia)}</h5>
                            <ul>
                    `;
                    
                    comidasPorDia[dia].forEach(comida => {
                        contenidoHTML += `<li>${comida.nombre} - ${comida.calorias} calorías</li>`;
                    });
                    
                    contenidoHTML += `
                            </ul>
                        </div>
                    `;
                }
            });
            
            contenidoHTML += `</div>`;
        }
        
        this.detallesContent.innerHTML = contenidoHTML;
        this.detallesModal.style.display = 'block';
    }
    
    /**
     * Elimina una dieta
     * @param {string} id - ID de la dieta a eliminar
     */
    eliminarDieta(id) {
        if (confirm('¿Estás seguro de que deseas eliminar esta dieta?')) {
            this.dietaService.eliminarDieta(id);
            this.cargarDietas();
            this.actualizarResumen();
        }
    }
    
    /**
     * Agrupa las comidas por día de la semana
     * @param {Array} comidas - Lista de comidas
     * @returns {Object} - Comidas agrupadas por día
     */
    agruparComidasPorDia(comidas) {
        const comidasPorDia = {};
        
        comidas.forEach(comida => {
            if (!comidasPorDia[comida.dia]) {
                comidasPorDia[comida.dia] = [];
            }
            
            comidasPorDia[comida.dia].push(comida);
        });
        
        return comidasPorDia;
    }
    
    /**
     * Capitaliza la primera letra de un texto
     * @param {string} texto - Texto a capitalizar
     * @returns {string} - Texto con primera letra en mayúscula
     */
    capitalizarPrimeraLetra(texto) {
        return texto.charAt(0).toUpperCase() + texto.slice(1);
    }
} 