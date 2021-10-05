import pandas as pd
import geopandas as gpd

RJ_UF_2020 = '/home/franreno/Documents/ic/munincipiosRJ/RJdata/RJ_RG_Intermediarias_2020/RJ_RG_Intermediarias_2020.shp'
RJ_RG_Intermediarias_2020 = '/home/franreno/Documents/ic/munincipiosRJ/RJdata/RJ_RG_Intermediarias_2020/RJ_RG_Intermediarias_2020.shp'
RJ_RG_Imediatas_2020 = '/home/franreno/Documents/ic/munincipiosRJ/RJdata/RJ_RG_Imediatas_2020/RJ_RG_Imediatas_2020.shp'
RJ_Municipios_2020 = '/home/franreno/Documents/ic/munincipiosRJ/RJdata/RJ_Municipios_2020/RJ_Municipios_2020.shp'
RJ_Microrregioes_2020 = '/home/franreno/Documents/ic/munincipiosRJ/RJdata/RJ_Microrregioes_2020/RJ_Microrregioes_2020.shp'
RJ_Mesorregioes_2020 = '/home/franreno/Documents/ic/munincipiosRJ/RJdata/RJ_Mesorregioes_2020/RJ_Mesorregioes_2020.shp'

FILENAME = '/home/franreno/Documents/ic/munincipiosRJ/RJdata/RJ_Municipios_2020/RJ_Municipios_2020.dbf'
aa = '/home/franreno/Downloads/rj_municipios/33MUE250GC_SIR.shp'
rj = gpd.read_file(aa)
print(rj)

