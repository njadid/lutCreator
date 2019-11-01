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
