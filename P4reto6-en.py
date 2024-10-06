# Translate to english
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import BytesIO  # Importar BytesIO
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime


# Usar el backend 'Agg' para evitar problemas con Streamlit
import matplotlib
matplotlib.use('Agg')

# List of causes
causas = [
    'Cause 1', 'Cause 2', 'Cause 3', 'Cause 4', 'Cause 5', 
    'Cause 6', 'Cause 7', 'Cause 8', 'Cause 9', 'Cause 10', 
    'Cause 11', 'Cause 12', 'Cause 13', 'Cause 14', 'Cause 15',
    'Cause 16', 'Cause 17', 'Cause 18', 'Cause 19', 'Cause 20',
    'Cause 21', 'Cause 22', 'Cause 23', 'Cause 24', 'Cause 25'
]

# Function to generate random frequencies
def generar_ejemplo():
    # Generate random frequncies betwen 10 y 25
    num_causas = np.random.randint(10, 26)
    causas_seleccionadas = np.random.choice(causas, size=num_causas, replace=False)
    
    # Split causes in 20% y 80%
    num_causas_20 = max(1, int(0.3 * num_causas))  # Al menos una causa estará en el 30%
    num_causas_80 = num_causas - num_causas_20
    
    # Design frequencies
    total_frecuencia = 600  # Total frequency (adjusble)
    
    # 80% of frequencies to 20% of causes
    frecuencias_20 = np.random.randint(50, 100, size=num_causas_20)  # Higest Frequencies
    frecuencias_20 = frecuencias_20 / frecuencias_20.sum() * 0.7 * total_frecuencia  # Escalar 80% of total
    
    # 20% of frequencies to 80% of causes
    frecuencias_80 = np.random.randint(1, 50, size=num_causas_80)  # Lowest Frequencies
    frecuencias_80 = frecuencias_80 / frecuencias_80.sum() * 0.2 * total_frecuencia  # Escalar 20% of total
    
    # Merge frequencies
    frecuencias = np.concatenate([frecuencias_20, frecuencias_80]).astype(int)
    
    # Create DataFrame with causes & frequencies
    df = pd.DataFrame({'Causa': causas_seleccionadas, 'Frecuencia': frecuencias})
    df = df.sort_values(by='Frecuencia', ascending=False)
    return df

# Configuration of navegation side bar
st.sidebar.title("Navegation")
page = st.sidebar.radio("Ir a:", ["Preview", "Pareto Chart", "Learning", "Next" ])

# Control de navegación con el estado de sesión
if "page" not in st.session_state:
    st.session_state.page = "Preview"

# Navigation Manager
if page == "Preview":
    st.session_state.page = "Preview"
elif page == "Pareto Chart":
    st.session_state.page = "Pareto Chart"
elif page == "Learning":
    st.session_state.page = "Learning"
elif page == "Next":
    st.session_state.page = "Next"

# Mostrar el contenido según la página seleccionada
if st.session_state.page == "Preview":
    # Página de inicio
    st.image("P4retoImage3.png", caption="Generate with Adobe Firefly & Canva", use_column_width=True)  # Ruta de la imagen local
    st.title("P4reto Chart 4.0")
    st.header('Instructions for Preparing Input Data to Create the Pareto Chart')
    st.markdown("""
                1. You must upload the data in an Excel file (.xlsx or .xls).
                2. Headers can be customized, but they must follow this order:
                - First column: place the categories (Failures, delays, threats, opportunities, causes). There is no character limit for this category, but a maximum of 25 characters maintains a readable appearance.
                - Second column: place the frequency (accumulated time for each event).
                - The chart title will be the file name without the extension.*
                - The sheet name will appear as a reference at the bottom of the chart.*
                - *In development
                3. There should be no blank cells or null values.
                4. The application will automatically sort event severity according to frequency in descending order.
                5. A unique feature of this interpretation of the Pareto chart is the shaded area corresponding to 80% of the stoppages. This greatly simplifies identifying the key areas that require more attention, which is why we call it the "Pay Attention Zone."
                6. We are excited to share that this simple differentiation has brought a couple of very valuable insights, which we will be developing in the coming days. As a challenge, we leave you with the following question: "How proactive or reactive do we consider ourselves?"
                """)
    
#if st.button("Ir a la Pareto Chart"):
    #st.session_state.page = "Pareto Chart"

elif st.session_state.page == "Pareto Chart":
    # Página de la Pareto Chart
    st.title("Failure Analysis Panel")
    st.write("Load data and automatly generate a Pareto Chart.")
    
    # Botón para cargar datos
    uploaded_file = st.file_uploader("Load Excel File", type=["xlsx"])

    # Inicializamos df_data como None
    df_data = None

    # Mostrar botón para generar ejemplo
    st.markdown("### Generate a random example")
    st.info("You can press the button to generate failure data and display the random chart.")
    # st.markdown("---")
    if st.button('Generate example'):
        df_data = generar_ejemplo()
        st.write("Example generated successfully")
        #st.dataframe(df_data)
    
    if uploaded_file is not None:
        # Si se ha cargado el archivo, leemos los datos en un DataFrame
        df_data = pd.read_excel(uploaded_file)
        df_data.rename(columns={df_data.columns[0]: 'Causa', df_data.columns[1]: 'Frecuencia'}, inplace=True)
        st.write("Data loaded successfully:")
        #st.dataframe(df_data)

    if df_data is not None:      
        # Procesar datos para el gráfico
        try:
            if 'Frecuencia' in df_data.columns and 'Causa' in df_data.columns:
                df_data['Porcentaje'] = df_data['Frecuencia'] / df_data['Frecuencia'].sum() * 100
                df_data = df_data.sort_values(by='Frecuencia', ascending=False)
                frecuencia_max = df_data['Frecuencia'].max()
                df_data['Porcentaje Acumulado'] = df_data['Porcentaje'].cumsum()
                
                # Pay Attention
                condicion = 80
                for i, valor in enumerate(df_data['Porcentaje Acumulado']):
                    if valor >= condicion:
                        xmax = i + 0.5
                        break
                xmin = -1    
                
                # Crear el gráfico de Pareto
                fig, ax = plt.subplots(figsize=(10, 6))
                plt.title('Pareto Chart 4.0', fontsize=14, pad=10)
                ax.bar(df_data['Causa'], df_data['Frecuencia'], color='blue')
                ax.set_xlabel("Causes")
                ax.set_ylabel("Frequency")
                ax.set_xticklabels(df_data['Causa'], rotation=90, fontsize=8)
                ax2 = ax.twinx()
                ax2.plot(df_data['Causa'], df_data['Porcentaje Acumulado'], color='red', linestyle='-')
                ax2.set_ylabel("% Accumulated")
                ax.axvspan(xmin, xmax, color='gray', alpha=0.3)
                ax.text(x= xmax-0.3, y= frecuencia_max, s='Pay Attention\nZone', fontsize=12, color='white', horizontalalignment='right', verticalalignment='top', alpha=0.5)
                plt.tight_layout()
                plt.xlim(-1, len(df_data))
                plt.ylim(0, 105)
                         
                st.write("### Pareto Chart 4.0")
                st.write("Events in the shaded area are responsible for 80% of the stoppages. Pay Attention!")
                st.pyplot(fig)

                # Descargar el gráfico como PDF
                pdf_buffer = BytesIO()
                with PdfPages(pdf_buffer) as pdf:
                    pdf.savefig(fig)
                    plt.close(fig)
            
                pdf_buffer.seek(0)
                st.download_button(
                    label="Dowload PDF Chart",
                    data=pdf_buffer,
                    file_name="pareto_chart.pdf",
                    mime="application/pdf"
                )

            else:
                st.warning("Make sure the file contains the correct columns: 'Cause', 'Frequency'.")
        except KeyError as e:
            st.warning(f"Error processing the data: {e}")
    else:
        # Si no se ha cargado el archivo, mostramos un mensaje
        st.write("### Waiting for data")
        st.info("Please upload an Excel file with the data or generate an example to visualize the chart.")

if st.session_state.page == "Learning":
    # Página Learning utilizar Pareto
    st.image("P4retoImage3.png", caption="Generated with Adobe Firefly & Canva", use_column_width=True)  # Ruta de la imagen local
    st.title("P4reto Chart 4.0")
    st.header('Instructions to Leverage New Insights from the Traditional Pareto Chart')
    st.markdown("""
                - Pareto is not a new tool; we do not intend to rework centuries of knowledge with this app. We already have enough sources of information that even we consulted in the development of this project. We will mention two links for those who are starting from scratch to consult and then return here with us.
                - Origin of the Pareto Principle: [https://en.wikipedia.org/wiki/Vilfredo_Pareto](https://en.wikipedia.org/wiki/Vilfredo_Pareto)
                - Origin of the Pareto Chart: [https://en.wikipedia.org/wiki/Pareto_chart](https://en.wikipedia.org/wiki/Diagrama_de_Pareto). The article is very comprehensive but contains a small transcription error, mentioning its creation at the beginning of the 1990s when, in reality, the chart was created in 1937, shortly before the start of the 1940s.
                - Since its creation, the elements of the Pareto chart have always been the same: Events, Frequency, and Cumulative Percentage. Subsequently, an analysis is performed on the 20% of events that theoretically cause 80% of the failures, and based on this analysis, plans are developed to correct the root cause of the deviations that generate these events, which cause delays or hinder our processes. Up to that point, everything is fine (we strongly believe in minimalist practices), but what was preventing us from having a bit more visual aid? We quickly answer that question with the reason that leads us to create and share this app: we discovered that it is a mix of technological limitations and creative conformity, as it is very simple to take a pencil and highlight which events fulfill the 80-20 relationship in the traditional Pareto chart. Additionally, using traditional graphing tools makes it a bit complicated to automatically highlight the area that we call the "Pay Attention Zone." With this combination of factors, the Pareto chart remained unchanged for almost 90 years.
                - "Pay Attention Zone" was initially a fleeting idea but unexpectedly unleashed an avalanche of insights that we will progressively develop. We will start with the basics, refreshing each traditional element and explaining in detail the importance of identifying and acting quickly on those events that most affect our processes...
                - We invite you to join us.
                 """)
    
    st.title("How to Interpret Correctly P4reto Chart 4.0")
    st.text("Let's study each element step by step.")
    st.image("P4retoImage4.png", caption="Generated with Adobe Firefly & Canva", use_column_width=True)  # Ruta de la imagen local
    st.header('Events')
    st.markdown("""
                # Events: Identification and Recording for Pareto Analysis
                - **What are events?** In the context of the Pareto chart, "events" refer to any occurrence, problem, or situation that interrupts or negatively affects a process. These events can vary depending on the industry or process being analyzed, but generally, events represent incidents that impact quality, productivity, or operational performance.
                - **Why is it important to record events?** The success of a Pareto analysis depends on the quality of the data that feeds the chart. A correct and complete record of events allows for a precise visualization of the most frequent or impactful causes in a process. In other words, identifying and recording key events is the first step in conducting an effective diagnosis that prioritizes corrective actions.
                - **Types of events to consider:** Depending on the industry and specific process, various types of events can be recorded. Below are some common examples in manufacturing and industrial maintenance:
                - **Machine downtimes:** A critical event is any unplanned downtime due to technical failures.
                - **Quality failures:** These are events where the final product does not meet the required specifications, resulting in waste or reprocessing.
                - **Production delays:** If a production process is delayed due to logistical or supply issues, it is important to record these events.
                - **Accidents or safety incidents:** In industries where safety is a priority, these events are crucial for identifying patterns and recurring causes.
                - **Maintenance failures:** Include all instances when equipment fails, whether due to mechanical, electrical, or other issues that require maintenance interventions.

                - **What events should NOT be recorded?** Often, there is a mistake of recording events that do not contribute to a meaningful analysis of the problem. Some examples of events that should not be considered in Pareto analysis are:
                - **Isolated or rare events:** Their impact on the system is minimal and do not generate a pattern worth addressing immediately.
                - **Minor or irrelevant issues:** Incidents that do not significantly affect quality or productivity.
                - **Events outside the control of the process:** If an event is not directly related to the internal operation of the process (e.g., an external infrastructure failure), it may distract from analyzing the true problem.

                - **Event Recording: Best Practices** To ensure an effective Pareto analysis, it is crucial to follow best practices in event recording:
                1. **Define clear criteria:** Determine what types of events should be recorded based on their impact on the process (frequency, severity, downtime, cost, etc.).
                2. **Maintain consistency:** Events should be recorded consistently, using clear and precise descriptions.
                3. **Recording tools:** Use maintenance or quality management software that allows for quick and efficient event recording.
                4. **Train staff:** It is essential that all personnel involved in the recording process understand the importance and criteria of the events to be recorded.

                These are general recommendations; we are aware that each process is different, and everyone must adapt to different circumstances and legal requirements. Common sense and good judgment should always prevail to ensure that the solution is not worse than the problem we are trying to solve.
                """)
    
    st.image("P4retoImage5.png", caption="Generated with Adobe Firefly & Canva", use_column_width=True)  # Ruta de la imagen local
    st.header('Frequency')
    st.markdown("""
                # Frequency: How to Measure the Repetition of Events

                **What is frequency in Pareto analysis?** Frequency refers to the number of times an event occurs over a specified period. It is one of the key parameters in the Pareto chart, as it helps us identify which events happen most regularly and therefore should receive greater attention when implementing corrective actions.

                **Importance of Frequency in Industry:** In an industrial environment, measuring the frequency of events such as equipment failures, production defects, or process interruptions is essential. The most frequent events tend to have the greatest impact on productivity or operational costs. For example, if the same failure in a machine occurs several times in a month, that event will likely have a higher priority for correction than a less frequent but severe event.

                **How to Record Frequency:** It is essential to have a reliable system for measuring how many times an event occurs. Here are some tips for tracking this:
                1. **Clearly define events:** As mentioned in the previous section, events should be well-defined to avoid confusion. For example, if we are measuring equipment failures, clear criteria must be established regarding what constitutes a failure that should be recorded.
                2. **Establish a time period:** Frequency should always be measured within a specific period, whether daily, weekly, or monthly, depending on the process being analyzed. This allows for more accurate comparisons and the detection of trends over time.
                3. **Use recording software:** Automated or semi-automated systems, such as CMMS (Computerized Maintenance Management Systems), can facilitate tracking the frequency of events, ensuring they are recorded quickly and accurately.
                4. **Ensure all relevant events are recorded:** Omitting an event can skew the analysis and make it difficult to identify the most frequent problems.

                **Examples of Frequency in Industry:**
                - **Mechanical failures:** If a component of a machine fails repeatedly over a week, its high frequency will be indicated on the Pareto chart, signaling that this part needs priority attention.
                - **Production defects:** If frequent failures are detected during a production process on a specific line, these recurring defects will be highlighted in the Pareto analysis.
                - **Workplace accidents:** In a safety-conscious environment, recording the frequency of incidents can help identify hazardous areas or unsafe practices.

                **How to Use Frequency in the Pareto Chart:** The Pareto chart visualizes the frequency of events through bars ordered from highest to lowest. Events that appear more frequently will have the tallest bars and will be the first considered for corrective actions. Additionally, "cumulative frequency" can be visualized through the Pareto curve, which helps identify what percentage of events (typically 80%) comes from a small number of causes (usually 20%).

                **Focus on Action:** The key is for attendees to understand that by identifying the most frequent events, they can act on them more quickly, allowing for improved productivity or preventing significant losses. Often, the most frequent events represent "quick wins" in terms of process improvement.

                ## Frequency vs. Impact (or Severity)

                **Frequency:** As mentioned, it refers to the number of times an event occurs within a specific period. However, an event that occurs very frequently but has a low impact may not be as much of a priority as one that occurs less frequently but has a much greater impact or severity.

                **Impact or Severity:** In this context, impact is mainly related to downtime or the magnitude of losses caused by an event. For example, a failure that halts production for 30 minutes will have a greater impact than one that causes a 5-minute interruption, even if the latter occurs more frequently.

                **The Dilemma: What to Prioritize?**
                - **High frequency, low severity:** These are events that occur regularly but have a relatively low impact. A classic example in maintenance is a low-criticality failure that does not halt the production process but causes minor interruptions.
                - **Low frequency, high severity:** These events are less common, but when they do occur, they generate significant impact, such as a serious accident or a total production stoppage that incurs high costs or safety risks.

                ## **Frequency-Severity Matrix:**

                A useful strategy is to combine both aspects into a matrix, where frequency and severity intersect. This allows for a clear visualization of which events should be prioritized for intervention:
                - **High frequency, high severity:** Maximum priority. Events that occur frequently and have a significant impact, such as frequent stoppages of critical machines.
                - **High frequency, low severity:** These events may be annoying but can be resolved with less urgent corrective actions. However, if they persist constantly, they can accumulate a significant impact over time.
                - **Low frequency, high severity:** Although these events are uncommon, they should have high priority, as the consequences of not addressing them in a timely manner can be severe.
                - **Low frequency, low severity:** These are the lowest priority events, as they do not significantly affect performance or safety.

                ## **Final Reflection**

                Often, we will have to deal with the frequency-severity duality in our Pareto analyses, making it very important to think beyond raw frequency and analyze the impact of events. One approach could be to learn how to calculate accumulated impact and how this can influence maintenance and production decisions.
                """)
    
    st.image("P4retoImage6.png", caption="Generated with Adobe Firefly & Canva", use_column_width=True)  # Ruta de la imagen local
    st.header('Attention')
    st.markdown("""
                # Pay Attention Zone

                The incorporation of the "Pay Attention Zone" represents a key innovation that is transforming our approach to data. Traditionally, the Pareto chart was limited to showing the 80/20 relationship by ordering events that generate the majority of problems in descending order. With the help of the Cumulative Percentage line, we could deduce the intersection of this relationship between Percentages and Events empirically. However, by automating the generation of a shaded area that visually highlights the events responsible for 80% of the downtimes, we have optimized this process. What started as a seemingly fleeting idea has proven to be a catalyst for new insights, offering a much deeper understanding of the underlying causes and how to resolve them.

                :rotating_light: Please take another look at the image that heads this section; "**Attention**" is the phase of the analysis that divides the past from the future. While each element of the analysis is important, "Attention" is particularly relevant because it concentrates both efforts: studying events, frequency, and severity (past), discovering causes, and implementing solutions (future). In this phase, the intervention of a specialist is indispensable. We have observed that omitting a specialist's participation severely affects the effectiveness of root cause analyses (**RCA**). Theory is fundamental to provide structure and method to the analysis, but without a detailed operational understanding, it is easy to fall into superficial solutions that do not address the root of the problem.

                The **"Pay Attention Zone"** we have implemented has the potential to visually highlight critical points directly. Still, if the individuals conducting the analysis lack practical knowledge and experience, we run the risk of misinterpreting the information or not delving deeply enough into the underlying causes.

                As an analogy, Sun Tzu said: **"Tactics without strategy are the noise before defeat."** In this context, we could say: **"Data analysis without practical knowledge is an empty exercise, doomed to failure."** This highlights how the Pareto analysis and the "Pay Attention Zone" can become powerful tools only if used correctly by those who understand both theory and practice. 
                :rotating_light:

                This "Pay Attention Zone" not only facilitates the interpretation of the chart but is also changing paradigms by allowing a more intuitive and quicker identification of critical events. This, in turn, has impacted the actions we take to resolve the root cause of problems, as it is now easier to prioritize interventions and resources. By placing greater emphasis on events within this zone, we can not only optimize traditional Pareto analysis but also develop new approaches that align better with the realities of operations and production.

                In summary, this simple change has opened a range of opportunities to restructure the analysis, helping to make more strategic and data-driven decisions, providing an even more powerful tool for continuous improvement in the industrial context. We know it may seem exaggerated to claim that a simple highlighted area can change paradigms, so we will better explain that assertion in the "Next" section of this app.
                """)
    
    st.image("P4retoImage7.png", caption="Generated with Adobe Firefly & Canva", use_column_width=True)  # Ruta de la imagen local
    st.header('Insights')
    st.markdown("""
                Once we have gathered enough evidence through the analysis of events and frequency, the next critical phase is the discovery of Insights. Insights are the key findings that allow us to understand the underlying causes behind each event. To reach this point, it is essential that the previous steps have been executed accurately, ensuring that the data is reliable and that there is an expert analyst who can carry out the attention phase with the necessary rigor.

                We consider it important to highlight that Pareto will help us find the most relevant or priority events that need immediate "attention." However, it is not a source of solutions; once opportunities are detected, a Root Cause Analysis (RCA) strategy must be implemented. This strategy includes different methodologies depending on the circumstances and characteristics of each particular process, and the most appropriate one must be selected. It is from this RCA analysis that our desired **Insights** will emerge.

                The Insight arises as a result of a deep and structured analysis, but one should not proceed without first validating the hypotheses. Here, it is crucial to verify the truth of each hypothesis formulated about the causes of the events. Additionally, the feasibility of possible solutions must be assessed, ensuring that they are practical and effective in the industrial context in which they will be applied. Skipping this stage can lead to implementing incorrect or ineffective actions, perpetuating problems rather than resolving them.

                The process of discovering an Insight is not only technical but also strategic, as it establishes the bridge between the collected data and the actions that will be taken to improve the system. Ensuring that Insights are accurate, based on true data and not mere assumptions, is key to success in the next phase of the Pareto analysis.
                """)
    
    st.image("P4retoImage8.png", caption="Generated with Adobe Firefly & Canva", use_column_width=True)  # Ruta de la imagen local
    st.header('Actions')
    st.markdown("""
                The Action Plan represents the culmination of all the previous analysis. This is where the recorded events, the frequency with which they occur, the attention given, and the discovered insights converge. The success of this plan directly depends on the accuracy with which the root cause of the events has been diagnosed. This means that the more thorough and precise the process has been, the better the results obtained in this phase.

                The Action Plan is not just a list of tasks; it is a structured guide that directly addresses the identified problems. For it to be effective, it must be based on solid data, an objective assessment, and a thorough verification of the hypotheses formulated in the previous phases. Each action must be aligned with the operational reality and adapted to the organization's capabilities, focusing on definitively resolving the causes that generated the events in the first place.

                Accuracy in diagnosing the underlying causes ensures that the Action Plan is directed at addressing the root problems, preventing recurrences and optimizing resources. Therefore, every step implemented must be well-justified, with a preventive, corrective, or improvement approach depending on the type of event and its impact. Prioritization is key here, focusing efforts on the critical events identified in the "Pay Attention Zone" to maximize results and achieve continuous improvement.
                """)

# Mostrar el contenido según la página seleccionada
if st.session_state.page == "Next":
    # Página de inicio
    st.title("P4reto Chart 4.0")
    st.header('Small changes can lead to great learnings!')
    st.markdown("""
                **Conscious of the apparent irrelevance that a simple shaded area, our "Pay Attention Zone," might have, we appeal to your curiosity and invite you to discover how much value this small detail can bring and how it can contribute to enriching the information we traditionally obtain from a classic tool like the Pareto chart.**
                - Since its creation, the Pareto chart has been a visual tool to highlight the events that cause 80% of our downtime. Today, thanks to technological advancements, we can automatically highlight that area (our "Pay Attention Zone") by simply adding five lines of code to the popular Python script that generates these types of charts. To our surprise, what began as a simple adjustment quickly revealed new insights, opening doors to broader opportunities.
                - By relating this small contribution to other studies, such as the potential/functional failure curve, we have begun to identify new opportunities, which we will progressively share in this application, as if it were a theoretical-practical blog.
                - Everyone is welcome to this adventure! Your comments, critiques, and contributions will be highly valued. We hope that **P4reto** is as useful for you as it is for us. We are at your disposal at: *elartedelmantenimientosuntzu@gmail.com*
                """)

# Obtener el día actual
hoy = datetime.now().day

# Mostrar el mensaje solo entre los días 29-05 de cada mes
if (29 <= hoy <= 31) or (1 <= hoy <= 5):
    st.markdown("""
        <hr>
        <p style='text-align: center; font-size: 12px;'>
            If you appreciate our work, consider making a donation via PayPal. - elartedelmantenimientosuntzu@gmail.com<br>
            "Gracias por contribuir con el proyecto"
        </p>
        """, unsafe_allow_html=True)


# streamlit run P4reto6-en.py