---
marp: true
size: 16:9
paginate: true
theme: default
backgroundColor: #aed6f1 
color:  #1a5276 
math: katex
_footer: hey
---

<style>section { justify-content: start; }</style>

<!-- backgroundImage: "linear-gradient(135deg, #ffffff  0%, #aed6f1 100%)" -->

<!-- 
_class: lead
_paginate: false
 -->

<style>
section { 
    font-size: 18px; 
}
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

<style scoped>section { font-size: 30px; justify-content: start;}</style>

# Clasificación de movimientos de CrossFit: una aplicación con MoViNets <!-- fit -->


**Agustín Piqueres** 

13/09/2022

![bg  50% w:40% h:30%](./assets/cidaen.png)
![bg w:200 h:100](./assets/logouclm.png)

<!-- footer: '![w:100 h:50](./assets/cidaen.png)' -->
<!-- _paginate: true -->

---


<!-- 
header : 'Clasificación de movimientos de CrossFit: una aplicación con MoViNets.'
-->

# 1.1 Motivación

Meter explicación de CrossFit (AQUÍ Y EN LA MEMORIA) y alguna imagen.

- Es un deporte con un gran número de participantes, y el número de competiciones sigue creciendo.

- Automatizando del proceso de corrección de videos:

  - Las personas pueden dejar una tarea repetitiva (se ahorra en personal).  

  - Se limitaría la inconsistencia entre distintos jueces en las correcciones.


---

# 1.2 Objetivos

Antes de llegar a ese punto, vamos a intentar crear una aplicación 
que sea capaz de clasificar movimientos de CrossFit,
para lo cuál será necesario:

- Crear un *Dataset* con movimientos de los distintos ejercicios. 

- Un modelo capaz de identificar correctamente los distintos movimientos.

- Una aplicación en la que un usuario sea capaz de subir un video 
y obtenga el movimiento del que se trata.


---


<style scoped>
div.twocols {
  margin-top: 35px;
  column-count: 2;
}
div.twocols p:first-child,
div.twocols h1:first-child,
div.twocols h2:first-child,
div.twocols ul:first-child,
div.twocols ul li:first-child,
div.twocols ul li p:first-child {
  margin-top: 0 !important;
}
div.twocols p.break {
  break-before: column;
  margin-top: 0;
}
</style>

<div class="twocols">

# 1.3 Estructura del proyecto

- **2 Estado del arte**

  - 2.1 Deep Learning
  - 2.2 Cloud
  - 2.3 Trabajos relacionados

- **3 Desarrollo**

  - 3.1 Extracción y recolección de datos
    - 3.1.1 Proceso de extracción
    - 3.1.2 Datos obtenidos

<p class="break"></p>

  <br><br>
  - 3.2 Experimentación con Deep Learning
    - 3.2.1 Preprocesado de los datos
    - 3.2.2 Experimentos realizados y resultados
    - 3.2.3 Evaluación de resultados

  - 3.3 Cloud y despliegue de la aplicación
    - 3.3.1 Arquitectura cloud
    - 3.3.2 Resultado y funcionamiento

- **4 Conclusiones**

</div>

---

# 2.1 Deep Learning

El campo del [*Reconocimiento de Acciones*](https://paperswithcode.com/task/action-recognition-in-videos) (la tarea de identificar personas realizando acciones en imágenes o videos) ha crecido en los años. Las acciones humanas pueden reconocerse con diferentes metodologías (como *Optical Flow* o representaciones del esqueleto), pero este trabajo se centra en la [*Clasificación de Video*](https://paperswithcode.com/task/video-classification):

La tarea de producir una etiqueta relevante para un video dados sus *frames*.

#### Lista de Papers:

- Primeros datasets: [HMDB51](https://serre-lab.clps.brown.edu/resource/hmdb-a-large-human-motion-database/) o [UCF101](https://www.crcv.ucf.edu/data/UCF101.php).

- Primer dataset para entrenar modelos de deep learning sobre 
clasificación de acciones en humanos: [Kinetics 400](http://arxiv.org/abs/1705.06950) (Modelo [I3D](http://arxiv.org/abs/1705.07750)).

- Uno de los modelos con resultados más prometedores es [MoViNets](https://arxiv.org/abs/2103.11511)
(actualmente ha habido grandes avances), una familia de modelos eficientes 
en el uso de memoria y computación, que permite operar con videos en streaming.

---

# 2.1 Deep Learning

<style scoped>
div.twocols {
  margin-top: 35px;
  column-count: 2;
}
div.twocols p:first-child,
div.twocols h1:first-child,
div.twocols h2:first-child,
div.twocols ul:first-child,
div.twocols ul li:first-child,
div.twocols ul li p:first-child {
  margin-top: 0 !important;
}
div.twocols p.break {
  break-before: column;
  margin-top: 0;
}
</style>

<div class="twocols">

## MoViNets

Esta familia de modelos se divida en 2 tipos diferentes de modelos: **base** y **stream**, según si procesan todo el video de golpe, o permiten procesar el contenido frame a frame, y en 5 arquitecturas distintas (desde *a0* hasta *a5*).

En este trabajo nos centramos en *MoViNet a2 base*, que es de entre los modelos más pequeños, el que tiene mejor capacidad predictiva y aún es capaz de ser utilizado en tiempo real (20 fps o más ([ref](https://blog.tensorflow.org/2022/04/video-classification-on-edge-devices.html)))

- No nos podemos centrar en los modelos stream, hay errores al hacer fine-tuning con ellos: [issue 10730](https://github.com/tensorflow/models/issues/10730) o [issue 10463](https://github.com/tensorflow/models/issues/10463#issuecomment-1019395406_).
- Los autores obtienen en tan solo 3 epochs un buen accuracy en UCF101.

<p class="break"></p>

<br>
<img src="./assets/thruster_prediction_stream.gif" 
      width="360" 
      height="360"
      />

*Ejemplo predicción en *MoViNet* Stream a2.*

</div>

---

# 2.2 Cloud

Todo el despliegue se ha realizado utilizando los distintos servicios
de AWS, sin recurrir a servicios como **AWS SageMaker**, **Azure ML** 
o **Google DataLab**, que ofrecen una solución completa al despliegue
de modelos basados en deep learning.

---

# 2.3 Trabajos relacionados

Un par de trabajos relacionados han tratado la clasificación de acciones:

- [Chen et al., 2022](https://www.mdpi.com/1424-8220/22/15/5700) hacen uso de Yolo4 para detectar y clasificar movimientos
de fitness.

- En un [artículo de towardsdatascience](https://towardsdatascience.com/how-i-created-the-workout-movement-counting-app-using-deep-learning-and-optical-flow-89f9d2e087ac) el autor hace uso de Optical Flow para
contar repeticiones de unos pocos movimientos.

*En otro [artículo de medium](https://blog.ml6.eu/sports-video-analysis-in-the-real-world-realtime-tennis-action-recognition-using-movinet-stream-813200aa589f) el autor hace fine tuning sobre uno de los modelos de MoViNets 
stream al parecer, pero no se puede ver el código ni hay forma de encontrar al autor.*

---

# 3.1 Extracción y Recolección de datos

## 3.1.1 Introducción

- Creación de un dataset de movimientos de CrossFit.

  - Descarga de los videos de YouTube.

  - Etiquetado.

- Análisis del *dataset*.


---

<style scoped>
div.twocols {
  margin-top: 35px;
  column-count: 2;
}
div.twocols p:first-child,
div.twocols h1:first-child,
div.twocols h2:first-child,
div.twocols ul:first-child,
div.twocols ul li:first-child,
div.twocols ul li p:first-child {
  margin-top: 0 !important;
}
div.twocols p.break {
  break-before: column;
  margin-top: 0;
}
</style>


<div class="twocols">

# 3.1 Extracción y Recolección de datos
## 3.1.2 Proceso de extracción

- `download.py`: Descarga de los videos de YouTube utilizando `yt-dlp`.

- [*Supervisely*](https://supervise.ly/): Software Open Source para *Computer Vision*, utilizado para el etiquetado de los vídeos.

- `manifester.py`: Script para la transformación del output de *Supervisely*, a un formato apto para el siguiente script: `manifest.json`.

- `ffmpeg-split.py`: Script para recortar los videos originales en mp4, para obtener los clips correspondientes a los frames etiquetados.

<p class="break"></p>

![center w:600 h:400](./assets/data_extraction_process_.png)

</div>


---


<style scoped>
div.twocols {
  margin-top: 35px;
  column-count: 2;
}
div.twocols p:first-child,
div.twocols h1:first-child,
div.twocols h2:first-child,
div.twocols ul:first-child,
div.twocols ul li:first-child,
div.twocols ul li p:first-child {
  margin-top: 0 !important;
}
div.twocols p.break {
  break-before: column;
  margin-top: 0;
}
</style>


<div class="twocols">

# 3.1 Extracción y Recolección de datos

## 3.1.3 Datos obtenidos

- $2700$ videos, $300$ ejemplos de cada movimiento en formato mp4, ~58 minutos de videos.

UCF101: 101 actividades, 131 muestras en media, alrededor de 13.000 clips, de unos 7 segundos de duración.


<p class="break"></p>

<br><br><br>

![image center](./assets/tabla_1_descriptive_stats.png)

</div>


---

<style scoped>
/* Reset table styling provided by theme */
table, tr, td, th {
  all: unset;

  /* Override contextual styling */
  border: 0 !important;
  background: transparent !important;
}
table { display: table; }
tr { display: table-row; }
td, th { display: table-cell; }

/* ...and layout freely :) */
table {
  width: 100%;
}
td {
  text-align: center;
  vertical-align: middle;
}
</style>

<!-- REF: 
https://github.com/marp-team/marp-cli/issues/57,
https://github.com/marp-team/marp-core/issues/155 
-->

# Ejemplo de los movimientos

<table>
  <tr>
    <td>thruster</td>
      <td><img src="./assets/thruster_1.gif" 
      width="180" 
      height="180"
      />
      </td>
    <td>chest-to-bar</td>
      <td><img src="./assets/chest-to-bar_1.gif" 
      width="180" 
      height="180"/>
      </td>
    <td>double-unders</td>
      <td><img src="./assets/double-unders_1.gif" 
      width="180" 
      height="180"/>
      </td>
  </tr>
  <tr>
    <td>ghd</td>
      <td><img src="./assets/ghd_1.gif" 
      width="180" 
      height="180"/>
      </td>
    <td>power clean</td>
      <td><img src="./assets/power-clean_1.gif" 
      width="180" 
      height="180"/>
      </td>
    <td>deadlift</td>
      <td><img src="./assets/deadlift_1.gif" 
      width="180" 
      height="180"/>
      </td>
  </tr>
  <tr>
    <td>shspu</td>
      <td><img src="./assets/shspu_1.gif" 
      width="180" 
      height="180"/>
      </td>
    <td>ohs</td>
      <td><img src="./assets/ohs_1.gif" 
      width="180" 
      height="180"/>
      </td>
    <td>bar-facing burpee</td>
      <td><img src="./assets/bar-facing-burpee_1.gif" 
      width="180" 
      height="180"/>
      </td>
  </tr>
</table>


---

# 3.2 Experimentación con Deep Learning

## 3.2.1 Introducción

- Selección del modelo

- Preprocesamiento de los datos

- Entrenamiento

- Resultados

---


<style scoped>
div.twocols {
  margin-top: 35px;
  column-count: 2;
}
div.twocols p:first-child,
div.twocols h1:first-child,
div.twocols h2:first-child,
div.twocols ul:first-child,
div.twocols ul li:first-child,
div.twocols ul li p:first-child {
  margin-top: 0 !important;
}
div.twocols p.break {
  break-before: column;
  margin-top: 0;
}
</style>


<div class="twocols">

# 3.2 Experimentación con Deep Learning

## 3.2.2 Preprocesado de los datos

- Librería para el preprocesamiento y fine-tuning:
 [`movinets_helper`](https://pypi.org/project/movinets_helper/)

  - [How To Guide](https://plaguss.github.io/movinets_helper/)

- Transformamos los datos originales a un nuevo [TFRecordDataset](https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset).

- Se reescalan los videos a una resolución de $224*224p$ (arquitectura *a2 base*), reescalado RGB $[0, 1]$.

- Muestra de $10 frames$ equiespacidos de cada video.

- El dataset pasa de ~400Mb -> ~10Gb(gzip).

<p class="break"></p>

<br><br><br>

![center w:650 h:300](./assets/frames.png)

</div>

---

<style scoped>
div.twocols {
  margin-top: 35px;
  column-count: 2;
}
div.twocols p:first-child,
div.twocols h1:first-child,
div.twocols h2:first-child,
div.twocols ul:first-child,
div.twocols ul li:first-child,
div.twocols ul li p:first-child {
  margin-top: 0 !important;
}
div.twocols p.break {
  break-before: column;
  margin-top: 0;
}
</style>


<div class="twocols">

# 3.2 Experimentación con Deep Learning

## 3.2.3 Experimentos realizados y resultados

- Entrenamiento en Google Colab con GPU.

- Mismos hiperparámetros que en el paper (tamaño batch $8$).

- 80% training ($2164$ clips), 20% test ($541$).

<p class="break"></p>

<br><br>

![center center w:600 h:300](./assets/sample_sizes.png)

<br>

* Resultados del entrenamiento: [*__Tensorboard.dev__*](https://tensorboard.dev/experiment/UXyupsnMQ2S74vdul3vdbw/#scalars)

</div>


---

<style scoped>section { font-size: 18px;}</style>

# 3.2 Experimentación con Deep Learning

## 3.2.4 Evaluación de los resultados


![bg center w:550 h:350](./assets/heatmap_confusion.png)

![bg center w:550 h:350](./assets/heatmap_correlations.png)


---

<style scoped>

div.twocols {
  margin-top: 35px;
  column-count: 2;
}
div.twocols p:first-child,
div.twocols h1:first-child,
div.twocols h2:first-child,
div.twocols ul:first-child,
div.twocols ul li:first-child,
div.twocols ul li p:first-child {
  margin-top: 0 !important;
}
div.twocols p.break {
  break-before: column;
  margin-top: 0;
}
</style>


<div class="twocols">

<style scoped>section { justify-content: start; }</style>

# 3.2 Experimentación con Deep Learning

## 3.2.4 Evaluación de los resultados


![left](./assets/tabla_2_estadisticos_probabilidades.png)


<p class="break"></p>

<br><br>

![w:600 h:400](./assets/probabilidades_estimadas_a1.png)

</div>


---


# 3.3 Cloud y despliegue de la aplicación

## 3.3.1 Introducción

- Arquitectura de la aplicación.

- Funcionamiento 

---

# 3.3 Cloud y despliegue de la aplicación
## 3.3.2 Arquitectura cloud

![center w:650 h:350](./assets/cloud_diagram.png)

- [`movinets_dash_app`](https://github.com/plaguss/movinets_dash_app)
- [lambda_aws](https://github.com/plaguss/tfm-misc/tree/main/lambda_aws).


---

# 3.3 Cloud y despliegue de la aplicación

## 3.3.3 Resultado y funcionamiento


app -> [movinet-crossfit-cidaen](DESPLEGAR_Y_PONER_DIRECCIÓN)

Mejoras:

- *post-training quantization*.

- Muestrear los videos como en la pipeline de entrenamiento.

- Utilizar un modelo más sencillo

---


<style scoped>

div.twocols {
  margin-top: 35px;
  column-count: 2;
}
div.twocols p:first-child,
div.twocols h1:first-child,
div.twocols h2:first-child,
div.twocols ul:first-child,
div.twocols ul li:first-child,
div.twocols ul li p:first-child {
  margin-top: 0 !important;
}
div.twocols p.break {
  break-before: column;
  margin-top: 0;
}
</style>


<div class="twocols">

<style scoped>section { justify-content: start; }</style>

# 3.3 Cloud y despliegue de la aplicación

## 3.3.3 Resultado y funcionamiento

![center w:300 h:200](./assets/bar-facing_burpee_example_app.png)
![center w:200 h:150](./assets/app_1.png)


<p class="break"></p>

<br><br><br><br>

![center w:300 h:200](./assets/app_2.png)
![center w:300 h:200](./assets/app_3.png)

</div>


---

# 4. Conclusiones

- Aplicación de *MoViNets* para la clasificación de movimientos de CrossFit.

- Creación de un nuevo dataset de clips de ejercicios de CrossFit etiquetados.

- Desarrollo de una aplicación en AWS para clasificar clips.

Siguientes pasos:

- Entrenamiento de arquitecturas *stream*.

- Metodologías alternativas como *Optical Flow*.

- Desplegar el modelo por medio de *Tensorflow Lite*.
