var basemap = new ol.layer.Tile({
    title: 'Basemap',
    source: new ol.source.OSM()
});

var basemap1 = new ol.layer.Tile({
    title: 'Basemap',
    source: new ol.source.OSM()
});

var administrateveBorders0 = new ol.layer.Vector({
    title: 'Districts',
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: 'data/crc/crc_districts.geojson'
    }),
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'rgba(1, 0, 0, 0.8)',
            width: 1
        }),
        fill: new ol.style.Fill({
            color: 'rgba(255, 120, 0, 0)'
        })
    })
});

var administrateveBorders1 = new ol.layer.Vector({
    title: 'Districts',
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: 'data/crc/crc_districts.geojson'
    }),
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'rgba(1, 0, 0, 0.8)',
            width: 1
        }),
        fill: new ol.style.Fill({
            color: 'rgba(255, 120, 0, 0)'
        })
    })
});


var fill = new ol.style.Fill({
    color: 'rgba(255,255,255,0.4)'
});
var stroke = new ol.style.Stroke({
    color: '#3399CC',
    width: 1.25
});
var stroke2 = new ol.style.Stroke({
    color: 'red',
    width: 1.25
});

var stroke3 = new ol.style.Stroke({
    color: 'yellow',
    width: 1.25
});

var stroke4 = new ol.style.Stroke({
    color: 'white',
    width: 1.25
});

var style1 = [
    new ol.style.Style({
        fill: fill,
        stroke: stroke
    })
];
var style2 = [
    new ol.style.Style({

        fill: fill,
        stroke: stroke2
    })
];

var style3 = [
    new ol.style.Style({

        fill: fill,
        stroke: stroke3
    })
];

var style4 = [
    new ol.style.Style({

        fill: fill,
        stroke: stroke4
    })
];



function transform(extent) {
    return ol.proj.transformExtent(extent, 'EPSG:4326', 'EPSG:3857');
}
const extents = {
    Copenhagen: transform([12.1, 55.55, 12.68, 55.82]),
    Krakow: transform([19.7832563712332004, 49.9441740986893308, 20.2313887895171476, 50.1543494107685959]),
};

var urbanity = new ol.layer.Vector({
    title: 'Urban Density',
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: 'data/crc/crc_residential.geojson',
        dataProjection: 'EPSG:3035',
        featureProjection: 'EPSG:3035'
    }),
    style: function(feature, resolution) {
        const age = feature.get('max_urbanity');
        if (age < 25) {
            return style1
        } else if (age >= 25 && age < 50) {
            return style2
        } else if (age >= 50 && age < 75) {
            return style3
        } else { return style4 }

        //return age < 50 ? style1 : style2;
    }
});


// EPSG:4326
proj4.defs('EPSG:3035', '+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +ellps=GRS80 +units=m +no_defs');
ol.proj.proj4.register(proj4);
var myProjection = new ol.proj.Projection({
    code: 'EPSG:3035',
    extent: ol.proj.get('EPSG:3035').getExtent()
});
const view = new ol.View({
    center: ol.proj.fromLonLat([19.95949, 50.03767]),

    zoom: 11
});

const map1 = new ol.Map({
    target: 'roadMap',
    layers: [basemap, administrateveBorders0, urbanity],
    view: view,
    projection: myProjection,
});

const map2 = new ol.Map({
    target: 'aerialMap',
    layers: [basemap1, administrateveBorders1],
    projection: myProjection,
    view: view
});

const OverlayPopup = document.querySelector('.overlay_popup');
const OverlayLayer = new ol.Overlay({
    element: OverlayPopup
})
map1.addOverlay(OverlayLayer);
const OverlayTreeName = document.getElementById('TreeName');
const OverlayTreeAge = document.getElementById('TreeAge');
console.log(OverlayLayer)
map1.on('click', function(e) {
    OverlayLayer.setPosition(undefined);
    map1.forEachFeatureAtPixel(e.pixel, function(feature, layer) {
        //console.log(e)
        console.log(feature, layer)
            /*
            var layer = trees.getLayer();
            var feature = layer.getFeatures();
            */
        let ClickCoordinate = e.coordinate;
        let varia = feature.getProperties()
        let ClickTreeName = varia.year;
        let ClickTreeAge = feature.get('nazwa');
        console.log(ClickTreeName)
        OverlayLayer.setPosition(ClickCoordinate);
        OverlayTreeName.innerHTML = '<p>District:' + ClickTreeAge + '</p>';
        if (typeof ClickTreeName !== "undefined") {
            OverlayTreeAge.innerHTML = '<p2>Completion:' + ClickTreeName + '</p>';
        }
        //OverlayTreeAge.innerHTML = '<p2>Completion:' + ClickTreeName + '</p>';
    })
});