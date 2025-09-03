import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd

data= pd.read_csv('munis.csv')
gdf= gpd.read_parquet("munis.parquet")

st.title("Primera aplicación")

munis = data ['entidad'].unique().tolist()
mun=st.selectbox ("seleccione un municipio:",
             munis)
filtro = data[data['entidad'] == mun]
             
#st.dataframe(filtro)
gen=( filtro.groupby ('clas_gen')['total_recaudo']
    .sum())

total_gen = gen.sum()
gen = (gen/ total_gen).round(2)

det= (filtro
      .groupby ('clasificacion_ofpuj') ['total_recaudo']
      .sum())
total_det = det.sum()
det= (det/ total_det).round(3)
                                
#st.dataframe(gen) #clasificacion general

#st.dataframe(det) # clasificacion detallada

##pie chart
#fig,ax = plt.subplots(1,1,figsize=(10,6))
#ax.pie(gen.values,labels= gen.index)

#st.pyplot(fig)
#fig,ax =plt.subplots (1,1,figsize = (10,6))
#ax.pie(det.values,labels=det.index)

#st.pyplot(fig)


#treemap
fin= (filtro
     .groupby(['clas_gen','clasificacion_ofpuj'])['total_recaudo']
     .sum()
     .reset_index())
#st.dataframe(fin)

fig= px.treemap(fin ,path =[px.Constant("Total"),
                            'clas_gen',
                            'clasificacion_ofpuj'],
                            values= 'total_recaudo')

st.plotly_chart(fig)
    


#pie chat1
fig1 = px.pie(
    names=gen.index,
    values=gen.values,
    title="distribucion general"
)
    
                 
st.plotly_chart(fig1)







# agregar un mapa 

filtro2 = gdf[gdf['entidad'] == mun][["codigo_alt","geometry"]]
fig, ax = plt.subplots(1,1)
filtro2.plot(ax=ax)
st.pyplot(fig)
