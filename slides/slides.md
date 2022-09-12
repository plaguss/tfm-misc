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

### 3.1 Extracción y Recolección de datos

#### 3.1.1 Introducción


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

### 3.1 Extracción y Recolección de datos
#### 3.1.2 Proceso de extracción

<p class="break"></p>

![center w:600 h:400](./assets/data_extraction_process_.png)

(Data extraction process)
</div>


---

### 3.1 Extracción y Recolección de datos

#### 3.1.3 Datos obtenidos

![image center](./assets/tabla_1_descriptive_stats.png)

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

* Ejemplo de los movimientos

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

### 3.2 Experimentación con Deep Learning

#### 3.2.1 Introducción


---

### 3.2 Experimentación con Deep Learning

#### 3.2.2 Preprocesado de los datos

![center w:1010 h:400](./assets/frames.png)

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

### 3.2 Experimentación con Deep Learning

#### 3.2.3 Experimentos realizados y resultados


- 80% training (2164 clips), 20% test (541)

- Más apuntes

<p class="break"></p>

![center center w:600 h:300](./assets/sample_sizes.png)

* [*__Tensorboard.dev__*](https://tensorboard.dev/experiment/UXyupsnMQ2S74vdul3vdbw/#scalars)

</div>


---

### 3.2 Experimentación con Deep Learning

#### 3.2.4 Evaluación de los resultados

<style scoped>section { font-size: 24px;}</style>

![bg center w:450 h:300](./assets/heatmap_confusion.png)

![bg center w:450 h:300](./assets/heatmap_correlations.png)

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

### 3.2 Experimentación con Deep Learning

#### 3.2.4 Evaluación de los resultados


![left](./assets/tabla_2_estadisticos_probabilidades.png)


<p class="break"></p>

![w:600 h:400](./assets/probabilities_by_movement.png)

</div>


---

## 3. Desarrollo

### 3.3 Cloud y despliegue de la aplicación

#### 3.3.1 Introducción


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

## 3.3  Desarrollo 
### 3.3 Cloud y despliegue de la aplicación
#### 3.3.2 Arquitectura cloud

<p class="break"></p>

![center w:600 h:400](./assets/cloud_diagram.png)(Diagrama Cloud) 
</div>


---

## 3. Desarrollo

### 3.3 Cloud y despliegue de la aplicación

#### 3.3.3 Resultado y funcionamiento

Poner link a la app y abrir para ver algún ejemplo.


---

## 4. Conclusiones




