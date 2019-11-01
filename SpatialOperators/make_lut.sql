SELECT  link_id, 
    grid_xy, 
    (grid_xy-100000000)/10000 x, 
    grid_xy%10000 y,
    sum(inter_area) inter_area,
    max(total_area) total_area,
    sum(contrib) contrib 
FROM (         --- pre
    SELECT  
        link_id, 
        grid_xy, 
        inter_area, 
        total_area, 
        inter_area/total_area contrib
    FROM (          --- h
        SELECT 
             link_id, 
             grid_xy, 
             ST_Area(
                ST_Intersection(
                   --- ST_Transform(
                     DH.geom, 
                   --- 4326
                   --- ), 
                   G.geom
                ), 
                true
             ) as inter_area,
             ST_Area(G.geom, true) as total_area
        FROM (  --- DH
                SELECT 
                    HS.* 
                FROM 
                    master_update M
                INNER JOIN 
                    env_geom_hillslope_single HS
                USING (link_id) WHERE model
            ) DH
        INNER JOIN 
        env_geom_grid_smap_ixy G ON 
        ST_Intersects(
            --- ST_Transform(
                DH.geom, 
            ---    4326
            ---), 
            G.geom)
        ) h 
    ) pre 
GROUP BY 
    link_id, 
    grid_xy;