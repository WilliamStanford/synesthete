import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd 
import matplotlib.pylab as pl
import numpy as np
import os

def plot_dataframe(ts_df):
  ts_df = ts_df.copy(deep=True)
  colors = pl.cm.inferno(np.linspace(0.1,.95,len(ts_df.columns)))
  fig, ax = plt.subplots(1,1,figsize=(6,4))
  fig.set_size_inches(10, 3)

  ts_df.plot(ax=ax, color=colors, alpha=.8)
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)
  ax.set_xlabel('Frames')  
  return fig

def plot_callback(ts_df, plot_placeholder, slider_inputs):

  ts_df = ts_df.copy(deep=True)
  for col, inp in zip(ts_df.columns, slider_inputs):
    ts_df[col] = ts_df[col]*inp

  plot_placeholder.write(plot_dataframe(ts_df))


def main():

  st.title("Synesthete.ai beta")
  st.header("Welcome")	

  user_path = 'Users/'
  user_input = st.text_input("Please enter your username", key='name')
  
  if st.session_state.name:

    user_input = str(user_input)
    os.makedirs(user_path + st.session_state.name, exist_ok=True)

    menu = ["Home", "Extract Audio Features", "Audio Features", "Generate Frames"]
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
      st.subheader('Default')

    if choice == 'Extract Audio Features':
      st.subheader('WIP')

    if choice == 'Audio Features':
      st.title('Audio Features')
  
      file_list = []
      for root, _, filenames in os.walk(user_path + st.session_state.name):
        for filename in filenames:
          file_list.append(os.path.join(root, filename).split('/')[-1])

      if len(file_list) == 0:
        st.header('No audio features extracted or uploaded')

      else:
        audio_choice = st.sidebar.selectbox('timeseries', file_list)
        ts_df = pd.read_csv(user_path + st.session_state.name + '/' + audio_choice, index_col=0)

        plot_placeholder = st.empty()
        plot_placeholder.write(plot_dataframe(ts_df))

        reset_df = st.button("reset coefficients")
        if reset_df:
          ts_df = pd.read_csv(user_path + st.session_state.name + '/coeffs.csv', index_col=0)
          plot_placeholder.write(plot_dataframe(ts_df))

          for col in ts_df.columns:
            st.session_state[col] = 1        

        with st.form(key='rescale'):
          slider_inputs = []
          for col in ts_df.columns:
            slider_inputs.append(st.slider(col, 0, 5, value=1, key=col))
    
          submit_button = st.form_submit_button(label='re-plot', on_click=plot_callback(ts_df, plot_placeholder, slider_inputs))

          
        coeff_ts = st.empty()
        coeff_ts = st.text_input("Input new filename and press enter to save", key='save_coeffs')
        
        if st.session_state.save_coeffs:
          ts_df.to_csv(user_path + st.session_state.name + '/' + str(coeff_ts) +'.csv', index=True)
          st.write('File saved')




    if choice == 'Generate Frames':
      print('WIP')


  
if __name__ == '__main__':
	main()
