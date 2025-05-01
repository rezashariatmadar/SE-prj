/**
 * Diagram Viewer Enhancement Script
 * Adds interactive features to diagrams including:
 * - Zoom in/out functionality
 * - Lightbox for full-screen viewing
 * - Interactive tooltips
 * - Smooth transitions between diagrams
 * - Responsive sizing
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all diagram containers
    initDiagramViewers();
});

/**
 * Initialize all diagram containers with enhanced functionality
 */
function initDiagramViewers() {
    const diagrams = document.querySelectorAll('.diagram-container img');
    
    diagrams.forEach((diagram, index) => {
        // Create wrapper if needed
        let container = diagram.parentElement;
        if (!container.classList.contains('diagram-container')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'diagram-container';
            diagram.parentNode.insertBefore(wrapper, diagram);
            wrapper.appendChild(diagram);
            container = wrapper;
        }
        
        // Add diagram controls
        addDiagramControls(container, diagram, index);
        
        // Add click event for lightbox
        diagram.addEventListener('click', function() {
            openLightbox(diagram.src, diagram.alt);
        });
        
        // Add hover tooltip if diagram has a description
        if (diagram.dataset.description) {
            addTooltip(container, diagram.dataset.description);
        }
    });
    
    // Create lightbox container if it doesn't exist
    if (!document.getElementById('diagram-lightbox')) {
        createLightboxContainer();
    }
}

/**
 * Add control buttons to diagram container
 */
function addDiagramControls(container, diagram, index) {
    const controlsDiv = document.createElement('div');
    controlsDiv.className = 'diagram-controls';
    
    // Zoom In button
    const zoomInBtn = document.createElement('button');
    zoomInBtn.innerHTML = '<i class="fas fa-search-plus"></i>';
    zoomInBtn.className = 'zoom-in-btn';
    zoomInBtn.title = 'Zoom In';
    zoomInBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        zoomDiagram(diagram, 1.2); // Scale up by 20%
    });
    
    // Zoom Out button
    const zoomOutBtn = document.createElement('button');
    zoomOutBtn.innerHTML = '<i class="fas fa-search-minus"></i>';
    zoomOutBtn.className = 'zoom-out-btn';
    zoomOutBtn.title = 'Zoom Out';
    zoomOutBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        zoomDiagram(diagram, 0.8); // Scale down by 20%
    });
    
    // Reset button
    const resetBtn = document.createElement('button');
    resetBtn.innerHTML = '<i class="fas fa-undo"></i>';
    resetBtn.className = 'reset-btn';
    resetBtn.title = 'Reset View';
    resetBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        resetDiagram(diagram);
    });
    
    // Fullscreen button
    const fullscreenBtn = document.createElement('button');
    fullscreenBtn.innerHTML = '<i class="fas fa-expand"></i>';
    fullscreenBtn.className = 'fullscreen-btn';
    fullscreenBtn.title = 'Fullscreen View';
    fullscreenBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        openLightbox(diagram.src, diagram.alt);
    });
    
    // Add buttons to controls div
    controlsDiv.appendChild(zoomInBtn);
    controlsDiv.appendChild(zoomOutBtn);
    controlsDiv.appendChild(resetBtn);
    controlsDiv.appendChild(fullscreenBtn);
    
    // Add controls to container
    container.appendChild(controlsDiv);
    
    // Add diagram id and data attributes for easier manipulation
    diagram.id = `diagram-${index}`;
    diagram.dataset.originalWidth = diagram.width || diagram.naturalWidth;
    diagram.dataset.originalHeight = diagram.height || diagram.naturalHeight;
    
    // Add caption if alt text exists
    if (diagram.alt && !container.querySelector('.diagram-caption')) {
        const caption = document.createElement('div');
        caption.className = 'diagram-caption';
        caption.textContent = diagram.alt;
        container.appendChild(caption);
    }
}

/**
 * Zoom diagram in or out by the specified scale factor
 */
function zoomDiagram(diagram, scaleFactor) {
    const currentWidth = parseInt(diagram.style.width) || diagram.width || diagram.naturalWidth;
    const currentHeight = parseInt(diagram.style.height) || diagram.height || diagram.naturalHeight;
    
    const newWidth = currentWidth * scaleFactor;
    const newHeight = currentHeight * scaleFactor;
    
    // Apply new dimensions with smooth transition
    diagram.style.width = `${newWidth}px`;
    diagram.style.height = `${newHeight}px`;
}

/**
 * Reset diagram to original size
 */
function resetDiagram(diagram) {
    const originalWidth = diagram.dataset.originalWidth;
    const originalHeight = diagram.dataset.originalHeight;
    
    diagram.style.width = originalWidth ? `${originalWidth}px` : '';
    diagram.style.height = originalHeight ? `${originalHeight}px` : '';
    diagram.style.transform = 'translate(0, 0)';
}

/**
 * Create lightbox container for fullscreen viewing
 */
function createLightboxContainer() {
    const lightbox = document.createElement('div');
    lightbox.id = 'diagram-lightbox';
    lightbox.className = 'diagram-lightbox';
    lightbox.style.display = 'none';
    
    const content = document.createElement('div');
    content.className = 'lightbox-content';
    
    const img = document.createElement('img');
    img.id = 'lightbox-img';
    
    const caption = document.createElement('div');
    caption.className = 'lightbox-caption';
    
    const closeBtn = document.createElement('button');
    closeBtn.className = 'lightbox-close';
    closeBtn.innerHTML = '&times;';
    closeBtn.addEventListener('click', closeLightbox);
    
    content.appendChild(img);
    content.appendChild(caption);
    lightbox.appendChild(content);
    lightbox.appendChild(closeBtn);
    
    // Close lightbox when clicking outside the image
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });
    
    document.body.appendChild(lightbox);
}

/**
 * Open lightbox with the selected diagram
 */
function openLightbox(src, alt) {
    const lightbox = document.getElementById('diagram-lightbox');
    const img = document.getElementById('lightbox-img');
    const caption = document.querySelector('.lightbox-caption');
    
    img.src = src;
    caption.textContent = alt || '';
    
    lightbox.style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Prevent scrolling
    
    // Add keyboard navigation
    document.addEventListener('keydown', handleLightboxKeyDown);
}

/**
 * Close the lightbox
 */
function closeLightbox() {
    const lightbox = document.getElementById('diagram-lightbox');
    lightbox.style.display = 'none';
    document.body.style.overflow = ''; // Restore scrolling
    
    // Remove keyboard event listener
    document.removeEventListener('keydown', handleLightboxKeyDown);
}

/**
 * Handle keyboard navigation in lightbox
 */
function handleLightboxKeyDown(e) {
    if (e.key === 'Escape') {
        closeLightbox();
    }
}

/**
 * Add tooltip to diagram
 */
function addTooltip(container, description) {
    const tooltip = document.createElement('div');
    tooltip.className = 'diagram-tooltip';
    tooltip.textContent = description;
    
    container.addEventListener('mouseenter', function() {
        tooltip.style.display = 'block';
    });
    
    container.addEventListener('mouseleave', function() {
        tooltip.style.display = 'none';
    });
    
    container.addEventListener('mousemove', function(e) {
        tooltip.style.left = `${e.pageX - container.offsetLeft + 10}px`;
        tooltip.style.top = `${e.pageY - container.offsetTop + 10}px`;
    });
    
    container.appendChild(tooltip);
} 