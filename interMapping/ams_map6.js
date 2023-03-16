var basemap = new ol.layer.Tile({
    title: 'Basemap',
    source: new ol.source.OSM()
});
var basemap1 = new ol.layer.Tile({
    title: 'Basemap',
    source: new ol.source.OSM()
});


const raster = new ol.layer.Tile({
    source: new ol.source.XYZ({
        attributions: 'Tiles © <a href="https://services.arcgisonline.com/ArcGIS/' +
            'rest/services/World_Topo_Map/MapServer">ArcGIS</a>',
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/' +
            'World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
    }),
});

const raster1 = new ol.layer.Tile({
    source: new ol.source.XYZ({
        attributions: 'Tiles © <a href="https://services.arcgisonline.com/ArcGIS/' +
            'rest/services/World_Topo_Map/MapServer">ArcGIS</a>',
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/' +
            'World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
    }),
});





var administrateveBorders0 = new ol.layer.Vector({
    title: 'Municipalities',
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: 'data/grootams/grootams_municipalities.geojson'
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
    title: 'Municipalities',
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: 'data/grootams/grootams_municipalities.geojson'
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
    width: 0.2
});
var stroke2 = new ol.style.Stroke({
    color: 'red',
    width: 0.2
});

var stroke3 = new ol.style.Stroke({
    color: 'yellow',
    width: 0.2
});

var stroke4 = new ol.style.Stroke({
    color: 'white',
    width: 0.2
});

var urban_style1 = [
    new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(0, 48, 73, 1)'
        }),
        stroke: new ol.style.Stroke({
            color: 'white',
            width: 0.2
        })
    })
];

var urban_style2 = [
    new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(214, 40, 40,1)'
        }),
        stroke: new ol.style.Stroke({
            color: 'white',
            width: 0.2
        })
    })
];

var urban_style3 = [
    new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(247, 127, 0,1)'
        }),
        stroke: new ol.style.Stroke({
            color: 'white',
            width: 0.2
        })
    })
];

var urban_style4 = [
    new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(252, 191, 73,1)'
        }),
        stroke: new ol.style.Stroke({
            color: 'white',
            width: 0.2
        })
    })
];

var year_style1 = [
    new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(0, 21, 36 ,1)'
        }),
        stroke: new ol.style.Stroke({
            color: 'white',
            width: 0.2
        })
    })
];

var year_style2 = [
    new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(0, 29, 89,1)'
        }),
        stroke: new ol.style.Stroke({
            color: 'white',
            width: 0.2
        })
    })
];

var year_style3 = [
    new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(0, 52, 136,1)'
        }),
        stroke: new ol.style.Stroke({
            color: 'white',
            width: 0.2
        })
    })
];

var year_style4 = [
    new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(0, 115, 204,1)'
        }),
        stroke: new ol.style.Stroke({
            color: 'white',
            width: 0.2
        })
    })
];

var year_style5 = [
    new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(224, 84, 0,1)'
        }),
        stroke: new ol.style.Stroke({
            color: 'white',
            width: 0.2
        })
    })
];

var year_style6 = [
    new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(253, 128, 33,1)'
        }),
        stroke: new ol.style.Stroke({
            color: 'white',
            width: 0.2
        })
    })
];

var year_style7 = [
    new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(255, 211, 115, 1)'
        }),
        stroke: new ol.style.Stroke({
            color: 'white',
            width: 0.2
        })
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
        url: 'data/grootams/grootams_residential_new.geojson',
        dataProjection: 'EPSG:3035',
        featureProjection: 'EPSG:3035'
    }),
    style: function(feature, resolution) {
        const age = feature.get('max_urbanity');
        if (age < 50) {
            return urban_style1
        } else if (age >= 50 && age < 75) {
            return urban_style2
        } else if (age >= 75 && age < 85) {
            return urban_style3
        } else { return urban_style4 }

        //return age < 50 ? style1 : style2;
    }
});

var urbanityIGC = new ol.layer.Vector({
    title: 'Urban Density',
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: 'data/grootams/grootams_residential_new.geojson',
        dataProjection: 'EPSG:3035',
        featureProjection: 'EPSG:3035'
    }),
    style: function(feature, resolution) {
        const age = feature.get('max_urbanity_igc');
        if (age < 55 && age > 0) {
            return urban_style1
        } else if (age >= 55 && age < 65) {
            return urban_style2
        } else if (age >= 65 && age < 75) {
            return urban_style3
        } else if (age >= 75 && age < 85) {
            return urban_style4
        } else { return urban_style5 }

        //return age < 50 ? style1 : style2;
    }
});



var compl_year = new ol.layer.Vector({
    title: 'Urban Density',
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: 'data/grootams/grootams_residential_new.geojson',
        dataProjection: 'EPSG:3035',
        featureProjection: 'EPSG:3035'
    }),
    style: function(feature, resolution) {
        const age = feature.get('year');
        if (age < 2025) {
            return year_style1
        } else if (age >= 2025 && age < 2030) {
            return year_style2
        } else if (age >= 2030 && age < 2035) {
            return year_style3
        } else if (age >= 2035 && age < 2040) {
            return year_style4
        } else if (age >= 2040 && age < 2045) {
            return year_style5
        } else if (age >= 2045 && age < 2050) {
            return year_style6
        } else { return year_style7 }

        //return age < 50 ? style1 : style2;
    }
});

var compl_year1 = new ol.layer.Vector({
    title: 'Urban Density',
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: 'data/grootams/grootams_residential_new.geojson',
        dataProjection: 'EPSG:3035',
        featureProjection: 'EPSG:3035'
    }),
    style: function(feature, resolution) {
        const age = feature.get('year_igc');
        if (age < 2025) {
            return year_style1
        } else if (age >= 2025 && age < 2030) {
            return year_style2
        } else if (age >= 2030 && age < 2035) {
            return year_style3
        } else if (age >= 2035 && age < 2040) {
            return year_style4
        } else if (age >= 2040 && age < 2045) {
            return year_style5
        } else if (age >= 2045 && age < 2050) {
            return year_style6
        } else { return year_style7 }

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
    center: ol.proj.fromLonLat([4.895267, 52.370673]),

    zoom: 11
});

const map1 = new ol.Map({
    target: 'bsMap',
    layers: [raster, administrateveBorders0, urbanity],
    view: view,
    projection: myProjection,
});

const map2 = new ol.Map({
    target: 'zmsMap',
    layers: [],
    projection: myProjection,
    view: view
});

const map3 = new ol.Map({
    target: 'warMap',
    layers: [],
    view: view,
    projection: myProjection,
});

const map4 = new ol.Map({
    target: 'igcMap',
    layers: [urbanityIGC],
    projection: myProjection,
    view: view
});

const map5 = new ol.Map({
    target: 'reMap',
    layers: [],
    projection: myProjection,
});

const map6 = new ol.Map({
    target: 'eurMap',
    layers: [],
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
        let ClickTreeAge = feature.get('GM_NAAM');
        console.log(ClickTreeName)
        OverlayLayer.setPosition(ClickCoordinate);
        OverlayTreeName.innerHTML = '<p>District:' + ClickTreeAge + '</p>';
        if (typeof ClickTreeName !== "undefined") {
            OverlayTreeAge.innerHTML = '<p2>Completion:' + ClickTreeName + '</p>';
        }
        //OverlayTreeAge.innerHTML = '<p2>Completion:' + ClickTreeName + '</p>';
    })
});