// You'll need to include these libraries in your HTML:
// <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
// <script src="https://cdnjs.cloudflare.com/ajax/libs/osmtogeojson/3.0.0-beta.4/osmtogeojson.js"></script>
// <script src="https://cdnjs.cloudflare.com/ajax/libs/dxf-writer/1.0.0/dxf-writer.min.js"></script>


async function generateDXFFromAddress(address) {
    try {
      // Step 1: Geocode the address
      const geocodeUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`;
      const geocodeResponse = await axios.get(geocodeUrl);
      if (geocodeResponse.data.length === 0) {
        throw new Error('Address not found');
      }
      const { lat, lon } = geocodeResponse.data[0];
  
      // Step 2: Fetch OSM data
      const osmUrl = `https://www.openstreetmap.org/api/0.6/map?bbox=${lon - 0.01},${lat - 0.01},${lon + 0.01},${lat + 0.01}`;
      const osmResponse = await axios.get(osmUrl);
      const geojson = osmtogeojson(osmResponse.data);
  
      // Step 3: Convert to DXF
      const drawing = new DxfWriter();
      geojson.features.forEach(feature => {
        if (feature.geometry.type === 'LineString') {
          const points = feature.geometry.coordinates.map(coord => ({x: coord[0], y: coord[1]}));
          drawing.addPolyline(points);
        } else if (feature.geometry.type === 'Polygon') {
          feature.geometry.coordinates.forEach(ring => {
            const points = ring.map(coord => ({x: coord[0], y: coord[1]}));
            drawing.addPolyline(points);
          });
        }
        // Add more geometry types as needed
      });
  
      // Step 4: Generate and download DXF file
      const dxfString = drawing.toDxfString();
      const blob = new Blob([dxfString], { type: 'application/dxf' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'map.dxf';
      link.click();
    } catch (error) {
      console.error('Error generating DXF:', error);
    }
  }
  
  // Usage
  const addressInput = document.getElementById('addressInput');
  const generateButton = document.getElementById('generateButton');
  
  generateButton.addEventListener('click', () => {
    const address = addressInput.value;
    generateDXFFromAddress(address);
  });
  