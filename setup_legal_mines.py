"""
Setup script: Create the legal_mines table in Supabase PostgreSQL
and populate it from the global_mining_polygons_v1.gpkg file.
"""
import psycopg2
import geopandas as gpd
from shapely.geometry import mapping
import json
import sys

DB_CONFIG = {
    'dbname'  : 'postgres',
    'user'    : 'postgres.ujjiugvcdgpljkaaqwwx',
    'password': 'harshatkare@1',
    'host'    : 'aws-1-ap-southeast-1.pooler.supabase.com',
    'port'    : 6543,
    'sslmode' : 'require',
}

GPKG_PATH = 'global_mining_polygons_v1.gpkg'

def main():
    # 1. Connect
    print("[1/4] Connecting to Supabase PostgreSQL...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        print("  Connected!")
    except Exception as e:
        print(f"  FAILED to connect: {e}")
        sys.exit(1)
    
    # 2. Check existing tables
    print("[2/4] Checking existing tables...")
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [r[0] for r in cur.fetchall()]
    print(f"  Tables found: {tables}")
    
    # 3. Check PostGIS extension
    print("[3/4] Ensuring PostGIS extension is available...")
    try:
        cur.execute("CREATE EXTENSION IF NOT EXISTS postgis")
        print("  PostGIS enabled!")
    except Exception as e:
        print(f"  PostGIS check: {e}")
    
    # 4. Create legal_mines table if it doesn't exist
    if 'legal_mines' in tables:
        cur.execute("SELECT COUNT(*) FROM legal_mines")
        count = cur.fetchone()[0]
        print(f"  legal_mines already exists with {count} rows.")
        if count > 0:
            print("  Skipping creation. Table is already populated.")
            cur.close()
            conn.close()
            return
        else:
            print("  Table exists but is empty. Will populate it.")
    else:
        print("[4/4] Creating legal_mines table...")
        cur.execute("""
            CREATE TABLE legal_mines (
                id SERIAL PRIMARY KEY,
                iso3_code TEXT,
                area DOUBLE PRECISION,
                geom_type TEXT,
                geom GEOMETRY(Geometry, 4326)
            )
        """)
        print("  Table created!")
    
    # 5. Load GPKG and insert 
    print(f"\n  Loading {GPKG_PATH}...")
    gdf = gpd.read_file(GPKG_PATH)
    print(f"  Loaded {len(gdf)} mining polygons")
    
    print("  Inserting into legal_mines (this may take a minute)...")
    inserted: int = 0
    failed: int = 0
    batch_size: int = 100
    
    for i in range(0, len(gdf), batch_size):
        batch = gdf.iloc[i:i+batch_size]
        values = []
        for _, row in batch.iterrows():
            try:
                geojson_str = json.dumps(mapping(row.geometry))
                values.append(cur.mogrify(
                    "(%s, %s, %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326))",
                    (row.get('ISO3_CODE', ''), row.get('AREA', 0), row.get('GEOM_TYPE', ''), geojson_str)
                ).decode())
            except Exception as e:
                failed += 1
                continue
        
        if values:
            try:
                cur.execute(
                    "INSERT INTO legal_mines (iso3_code, area, geom_type, geom) VALUES " + ",".join(values)
                )
                inserted += int(len(values))  # pyre-ignore
            except Exception as e:
                print(f"  Batch insert error: {e}")
                failed += int(len(values))  # pyre-ignore
        
        if (i + batch_size) % 1000 == 0 or i + batch_size >= len(gdf):
            print(f"    Progress: {min(i+batch_size, len(gdf))}/{len(gdf)} (inserted={inserted}, failed={failed})")
    
    # 6. Create spatial index
    print("\n  Creating spatial index...")
    try:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_legal_mines_geom ON legal_mines USING GIST (geom)")
        print("  Spatial index created!")
    except Exception as e:
        print(f"  Index error: {e}")
    
    # Final check
    cur.execute("SELECT COUNT(*) FROM legal_mines")
    final_count = cur.fetchone()[0]
    print(f"\n  DONE! legal_mines table has {final_count} rows.")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
