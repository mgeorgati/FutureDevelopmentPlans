<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.10.1-A Coruña" maxScale="0" styleCategories="AllStyleCategories" minScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
  </customproperties>
  <pipe>
    <rasterrenderer classificationMin="1" band="1" type="singlebandpseudocolor" alphaBand="-1" classificationMax="inf" opacity="1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader classificationMode="2" clip="0" colorRampType="DISCRETE">
          <colorramp type="gradient" name="[source]">
            <prop k="color1" v="0,0,255,255"/>
            <prop k="color2" v="0,255,0,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
          </colorramp>
          <item value="1" color="#f7fbff" label="&lt;= 1" alpha="0"/>
          <item value="2000" color="#e2ebf3" label="1 - 2000" alpha="255"/>
          <item value="5000" color="#9ac8e0" label="2000 - 5000" alpha="255"/>
          <item value="10000" color="#529dcc" label="5000 - 10000" alpha="255"/>
          <item value="20000" color="#1d6cb1" label="10000 - 20000" alpha="255"/>
          <item value="inf" color="#08306b" label="> 20000" alpha="255"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="200" contrast="0"/>
    <huesaturation colorizeRed="255" colorizeGreen="128" colorizeStrength="100" grayscaleMode="0" saturation="0" colorizeBlue="128" colorizeOn="0"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>12</blendMode>
</qgis>
