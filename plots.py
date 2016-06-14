import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
#CMAQ Spatial Plots
def make_spatial_plot(cmaqvar,gridobj,date,m,dpi=None,savename=''):
    from numpy import arange
    fig = plt.figure(figsize=(12,6),frameon=False)
    lat = gridobj.variables['LAT'][0, 0, :, :].squeeze()
    lon = gridobj.variables['LON'][0, 0, :, :].squeeze()
    #define map and draw boundries
    m.drawstates();m.drawcoastlines();m.drawcountries()
    x,y = m(lon,lat)
    plt.axis('off')

    cmap = plt.cm.get_cmap('viridis')
    norm = normval(0,150.,cmap)
    m.pcolormesh(x,y,cmaqvar,norm=norm,cmap=cmap)
    titstring = date.strftime('%B %d %Y %H')
    plt.title(titstring)

    c = plt.colorbar(ticks=arange(0,150,5)+2.5)
    c.set_ticklabels([str(s) for s in arange(0,150,5)+5])

    plt.tight_layout()
    if savename!='':
        plt.savefig(savename+date.strftime('%Y%m%d_%H.jpg'),dpi=dpi)
        plt.close()
    return c

def normval(vmin,vmax,cmap):
    from numpy import arange
    from matplotlib.colors import BoundaryNorm
    bounds = arange(vmin,vmax,5.)
    norm = BoundaryNorm(boundaries=bounds,ncolors=cmap.N)
    return norm

#Spatial Plotting of AQS on basemap instance m
def aqs_spatial_scatter(aqs, m, date, savename=''):
    new = aqs[aqs.datetime == date]
    x, y = m(new.Longitude.values, new.Latitude.values)
    cmap = plt.cm.get_cmap('viridis')
    norm = normval(0,150.,cmap)
    plt.scatter(x, y, c=new['Obs_value'].values, norm=norm, cmap=cmap)
    if savename != '':
        plt.savefig(savename + date + '.jpg', dpi=75.)
        plt.close()


#Spatial Plotting of Improve on maps
def improve_spatial_scatter(improve,m,date,param,vmin=None,vmax=None,cmap='viridis',savename=''):
    new = improve[improve.datetime == date]
    x,y = m(new.Lon.values,new.Lat.values)
    plt.scatter(x,y,c=new[param].values,vmin=vmin,vmax=vmax,cmap=cmap)
    if savename != '':
        plt.savefig(savename + date + '.jpg',dpi=75.)
    plt.close()



#Time series implementation for AQS
def plot_timeseries(dataframe,domain_ave=True,ylabel='PM10 Concentration',savename='',title='',convert=True):
    import gc
    #format plot stuff
    sns.set_style('whitegrid')
    if convert:
        dataframe['Obs_value'] *= 1000.
    if domain_ave:
        domainave = dataframe.groupby('datetime').mean()
        plt.plot(domainave.index.values,domainave['Obs_value'].values,'k',label='OBS')
        plt.plot(domainave.index.values,domainave['cmaq'].values,label='CMAQ')
        plt.ylabel(ylabel)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        plt.xticks(rotation=30)
        plt.title( title)
        plt.tight_layout()
        plt.legend(loc='best')
        if savename != '':
            plt.savefig(savename+'_average.jpg',dpi=100)
            plt.close()
    else:
        plt.plot(dataframe.index,dataframe['Obs_value'],'k',label='OBS')
        plt.plot(dataframe.index,dataframe['cmaq'],label='CMAQ')
        plt.ylabel(ylabel)
        plt.xticks(rotation=30)
        plt.title(title)
        plt.tight_layout()
        plt.legend(loc='best')
        if savename != '':
            plt.savefig(savename+ str(dataframe['SCS'].unique()[0])+ '.jpg',dpi=100)
            plt.close()

    gc.collect()

#Plot each site in the AQS dataframe
def plot_allsites_timeseries(dataframe,ylabel='PM10 Concentration',savename=''):
    sites = dataframe.SCS.unique()
    dataframe.index = dataframe.datetime
    for i in sites:
        sitedf = dataframe[dataframe['SCS'] == i]
        plot_timeseries(sitedf,siteave=False,ylabel=ylabel,savename=savename)
    plot_timeseries(dataframe,siteave=True,ylabel=ylabel,savename=savename)

