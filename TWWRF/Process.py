# Regrid Wind Speed Value from EAR5 to WRF
# The WRF dataset was recorded in 2D-Latitude and 2D-Longitude.
# The WRA5 dataset was recorded in 1D-Latitude and 1D-Longitude.
def era2wrf(ERA5_Path, WRF_Path, Variable):
    import numpy as np
    import xarray as xr
    ERA5 = xr.open_dataset(ERA5_Path,decode_times=False)
    WRF = xr.open_dataset(WRF_Path,decode_times=False)
    L_map_lon = ERA5['longitude'].values
    L_map_lat = ERA5['latitude'].values
    nav_lon = WRF['nav_lon'].values
    nav_lat = WRF['nav_lat'].values
    nx_1 = len(WRF['x'])-1
    ny_1 = len(WRF['y'])-1
    ERA5_var = ERA5["{}".format(Variable)].values
    New_map = np.zeros((ERA5_var.shape[0], WRF.dims["y"], WRF.dims["x"]))
    for t in range(ERA5_var.shape[0]):
        for x in range(WRF.dims["x"]):
            for y in range(WRF.dims["y"]):

                Left_lon = np.where(nav_lon[y][x]<L_map_lon)[0][0] 
                Right_lon = np.where(L_map_lon<nav_lon[y][x])[0][-1]
                Lower_lat = np.where(nav_lat[y][x]<L_map_lat)[0][-1]
                Upper_lat = np.where(L_map_lat<nav_lat[y][x])[0][0]

                Dist_LL = np.sqrt((nav_lon[y][x]-L_map_lon[Left_lon])**2+(nav_lat[y][x]-L_map_lat[Lower_lat])**2)
                Dist_LU = np.sqrt((nav_lon[y][x]-L_map_lon[Left_lon])**2+(nav_lat[y][x]-L_map_lat[Upper_lat])**2)
                Dist_RL = np.sqrt((nav_lon[y][x]-L_map_lon[Right_lon])**2+(nav_lat[y][x]-L_map_lat[Lower_lat])**2)
                Dist_RU = np.sqrt((nav_lon[y][x]-L_map_lon[Right_lon])**2+(nav_lat[y][x]-L_map_lat[Upper_lat])**2)

                Dist = [Dist_LL, Dist_LU, Dist_RL, Dist_RU]
                Dist_min = Dist.index(np.min(Dist))
                if Dist_min==0:
                    New_map[t,y,x]=ERA5_var[t,Lower_lat,Left_lon]
                elif Dist_min==1:
                    New_map[t,y,x]=ERA5_var[t,Upper_lat,Left_lon]
                elif Dist_min==2:
                    New_map[t,y,x]=ERA5_var[t,Lower_lat,Right_lon]
                elif Dist_min==3:
                    New_map[t,y,x]=ERA5_var[t,Upper_lat,Right_lon]
    return New_map


def Spilt_Area():
    import numpy as np
    import pandas as pd
    ## Taiwan County X, Y
    TW_County_Grid = pd.read_excel('WRF_TW_County_grid_T97.xlsx')

    ## County_Arrange (North -> South, West -> East)
    CN = ["Keelung_City", "Taipei_City", "New_Taipei_City", "Taoyuan_City", "Hsinchu_City", "Hsinchu", "Miaoli", "Taichung_City",
          "Nantou", "Changhua", "Yunlin", "Chiayi_City", "Chiayi", "Tainan_City", "Kaohsiung_City", "Pingtung", "Yilan",
          "Hualien","Taitung"]
    ## Area_filter ##Block_Mask
    taiwan_array = np.zeros((19, 86, 41)) # 19 Area
    taiwan_array[:] = np.nan

    area_mark = np.zeros((86, 41))
    area_mark[:] = np.nan

    block_x = TW_County_Grid.x
    block_y = TW_County_Grid.y

    County = {}

    for n in range(19):
        for i in range(len(TW_County_Grid)):
            if TW_County_Grid.NO[i] == n+1:
                taiwan_array[n, block_y[i]-1, block_x[i]-1] = 1
                area_mark[block_y[i]-1, block_x[i]-1] = n+1
                County[CN[n]]=taiwan_array[n]
    return County


class TW_County:    
    def __init__(self, dataset):  
        County = Spilt_Area()
        self.Keelung_City = County["Keelung_City"]*dataset
        self.Taipei_City = County["Taipei_City"]*dataset
        self.New_Taipei_City = County["New_Taipei_City"]*dataset
        self.Hsinchu_City = County["Hsinchu_City"]*dataset
        self.Hsinchu = County["Hsinchu"]*dataset
        self.Miaoli = County["Miaoli"]*dataset
        self.Taichung_City = County["Taichung_City"]*dataset
        self.Nantou = County["Nantou"]*dataset
        self.Changhua = County["Changhua"]*dataset
        self.Yunlin = County["Yunlin"]*dataset
        self.Chiayi_City = County["Chiayi_City"]*dataset
        self.Chiayi = County["Chiayi"]*dataset
        self.Tainan_City = County["Tainan_City"]*dataset
        self.Kaohsiung_City = County["Kaohsiung_City"]*dataset
        self.Pingtung = County["Pingtung"]*dataset
        self.Chiayi = County["Chiayi"]*dataset
        self.Yilan = County["Yilan"]*dataset
        self.Hualien = County["Hualien"]*dataset         
        self.Taitung = County["Taitung"]*dataset  
