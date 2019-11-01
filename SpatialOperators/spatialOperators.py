import gdal
import ogr
import osr
import os
import numpy as np

class LUTGen:
    def rast2shpgrid(fn):
        # fn = 'smapvex_data/SM_hpol_20160528.tif'
        sourceRaster = gdal.Open(fn)
        band = sourceRaster.GetRasterBand(1)
        geotransf = sourceRaster.GetGeoTransform()
        srs = osr.SpatialReference()
        srs.ImportFromWkt(sourceRaster.GetProjection())
        # print geotransf
        [row, col] = np.shape(band.ReadAsArray())
        # test with rand values
        data1d = np.asarray(range(0, col*row))
        data1d = data1d.reshape(row, col)

    def writeFile(filename, geotransform, geoprojection, data):
        (x, y) = data.shape
        format = "GTiff"
        driver = gdal.GetDriverByName(format)
        # you can change the dataformat but be sure to be able to store negative values including -9999
        dst_datatype = gdal.GDT_Float32
        dst_ds = driver.Create(filename, y, x, 1, dst_datatype)
        dst_ds.GetRasterBand(1).WriteArray(data)
        dst_ds.SetGeoTransform(geotransform)
        dst_ds.SetProjection(geoprojection)
        dst_ds.GetRasterBand(1).SetNoDataValue(-9999)
        return 1

    # filename = 'out.tif'
    _fn_out = os.path.abspath(fn)
    fn_out = _fn_out[:-4] + '_numbered.tif'
    geoprojection = sourceRaster.GetProjection()
    writeFile(fn_out, geotransf, geoprojection, data1d)

    sourceRaster = gdal.Open(fn_out)
    band = sourceRaster.GetRasterBand(1)
    outShapefile = _fn_out[:-4] + '_numbered'
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(outShapefile+".shp"):
        driver.DeleteDataSource(outShapefile+".shp")
    outDatasource = driver.CreateDataSource(outShapefile + ".shp")
    outLayer = outDatasource.CreateLayer("polygonized", srs=srs)
    gdal.Polygonize(band, None, outLayer, -1, [], callback=None)
    outDatasource.Destroy()
    sourceRaster = None
#%%
    def testProjection:
        import gdal, osr
        import ogr
        ds = gdal.Open(r'srtm_18_03/srtm_18_03.tif')
        prj = ds.GetProjection()
        ds.pol
        print
        prj

        srs = osr.SpatialReference(wkt=prj)
        if srs.IsProjected:
            print
            srs.GetAttrValue('projcs')
        print
        srs.GetAttrValue('geogcs')

#%%
    def read_shp(fn):
        driver = ogr.GetDriverByName('ESRI Shapefile')
        # from Layer
        inDataSet = driver.Open(fn)
        # print inDataSet
        # inLayer = inDataSet.GetLayer()
        return inDataSet

    p1 = read_shp(
        '/Users/navid/Documents/OneDrive - University of Iowa/Research/lut_tutorial/smapvex_data/SM_hpol_20160528_numbered_reproj.shp')

    p2 = read_shp(
        '/Users/navid/Documents/OneDrive - University of Iowa/Research/lut_tutorial/smapvex_data/basemap_4326.shp')
    layer = p1.GetLayer()

    for feature in layer:
        geom = feature.GetGeometryRef()


#%%
from osgeo import ogr
ogr.UseExceptions()
ogr_ds = ogr.Open('data', True)  # Windows: r'C:\path\to\data'
SQL = """\
    SELECT ST_Intersection(A.geometry, B.geometry) AS geometry, A.*, B.*
    FROM sf_hs A, SM_hpol_20160528_numbered_reproj B
    WHERE ST_Intersects(A.geometry, B.geometry);
"""
layer = ogr_ds.ExecuteSQL(SQL, dialect='SQLITE')
# copy result back to datasource as a new shapefile
layer2 = ogr_ds.CopyLayer(layer, 'h1_buf_int_ct4')
# save, close
layer = layer2 = ogr_ds = None
 #%%
 #test
from polygonize import rast2shpgrid
from reproject_layers import reproject_shp
fn = 'smapvex_data/SM_hpol_20160528.tif'
out_sp_ref = 4326

rast2shpgrid(fn)
reproject_shp(fn, out_sp_ref)
#%% or shapely

from shapely.geometry import Polygon
polys = [ Polygon(((0, 0), (1, 0), (1, 1))), Polygon(((0, 1), (0, 0), (1, 0))), Polygon(((100, 100), (101, 100), (101, 101))) ]
s = STRtree(polys)
query_geom = Polygon(((-1, -1), (2, 0), (2, 2), (-1, 2)))
result = s.query(query_geom)
polys[0] in result