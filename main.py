import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import io

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Hey Jose"))

# 5 num sum function
def calculate_five_number_summary(data):
    min_val = np.min(data)
    max_val = np.max(data)
    median = np.median(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    return min_val, q1, median, q3, max_val
# Proportions of category function
def calculate_proportions(data):
    proportions = data.value_counts(normalize=True)
    return proportions


if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")
    display_relevant_statistics = st.checkbox("Display Relevant Statistics")

    if show_df:
      st.write(df)

    if display_relevant_statistics:
      st.write("Dataset shape:", df.shape)

    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical", "Bool", "Date"))

    if column_type == "Numerical":
      numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)
      st.write("Selected column:", numerical_column)
      st.write(df[numerical_column])
      min_val, q1, median, q3, max_val = calculate_five_number_summary(df[numerical_column])
      st.write("Selected column five number summary:")
      five_num_sum_data = pd.DataFrame({
            'Statistic': ['Min', 'Q1', 'Median', 'Q3', 'Max'],
            'Value': [min_val, q1, median, q3, max_val]
        })
      st.table(five_num_sum_data)
      
      # histogram
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)

      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Histogram')
      hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

      fig, ax = plt.subplots()
      ax.hist(df[numerical_column], bins=hist_bins,
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )

    if column_type == "Categorical":
      catagorical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['object']).columns)
      st.write("Selected column:", catagorical_column)
      st.write(df[catagorical_column])

      # proporttions 
      proportions = calculate_proportions(df[catagorical_column])
            
      st.write("Category Proportions:")
      st.table(proportions)
            
      # Create a bar plot
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)

      bar_title = st.text_input('Set Title', 'Bar Plot')
      bar_xtitle = st.text_input('Set x-axis Title', catagorical_column)
      
      plt.bar(proportions.index, proportions.values, edgecolor = "black", color = choose_color, alpha = choose_opacity)
      plt.xlabel(bar_xtitle)
      plt.ylabel("proportion")
      plt.title(bar_title)
      st.pyplot(plt)
      
      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )

if web_apps == "Hey Jose":
  st.write('Jose! Hey.')