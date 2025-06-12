'''
    This file contains the code for the bubble plot.
'''

import plotly.express as px

import hover_template


def get_plot(my_df, gdp_range, co2_range):
    '''
        Generates the bubble plot.

        The x and y axes are log scaled, and there is
        an animation between the data for years 2000 and 2015.

        The discrete color scale (sequence) to use is Set1 (see : https://plotly.com/python/discrete-color/)

        The markers' maximum size is 30 and their minimum
        size is 6.

        Args:
            my_df: The dataframe to display
            gdp_range: The range for the x axis
            co2_range: The range for the y axis
        Returns:
            The generated figure
    '''
    # TODO : Define figure with animation

    fig = px.scatter(
        my_df,
        x = "GDP",
        y="CO2",
        log_x=True,
        log_y=True,
        color_discrete_sequence=px.colors.qualitative.Set1,
        range_x=gdp_range,
        range_y=co2_range,
        size_max=30,
        color='Continent',
        size='Population',
        animation_frame='Year',
        animation_group='Country Name',
        hover_name='Country Name',
        custom_data=['Population']

    )

    fig.update_traces(marker=dict(sizemin=6))
    
    return fig


def update_animation_hover_template(fig):
    '''
        Sets the hover template of the figure,
        as well as the hover template of each
        trace of each animation frame of the figure

        Args:
            fig: The figure to update
        Returns:
            The updated figure
    '''

    # TODO : Set the hover template
    for frame in fig.frames:
        for trace in frame.data:
            trace.update(hovertemplate=hover_template.get_bubble_hover_template())


    return fig


def update_animation_menu(fig):
    '''
        Updates the animation menu to show the current year, and to remove
        the unnecessary 'Stop' button.

        Args:
            fig: The figure containing the menu to update
        Returns
            The updated figure
    '''
    # TODO : Update animation menu

    fig.update_layout(
        updatemenus = [
            {
                'direction': 'left',
                'buttons' : [
                    {
                        'label' : 'Animate',
                        'method' : 'animate',
                       'args': [None],
                    },
                    {
                        "label": "Pause",
                        'method' : 'animate',
                        'args': [None],
                        'visible': False 
                    }
                    
                ],
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }
        ]
    )

    sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 12},
        "prefix": "Data for year:",
        "visible": True,
        "xanchor": "left"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
    }

    fig.update_layout(sliders=[sliders_dict])



    return fig


def update_axes_labels(fig):
    '''
        Updates the axes labels with their corresponding titles.

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    # TODO : Update labels

    fig.update_xaxes(title_text='GDP per capita ($ USD)')
    fig.update_yaxes(title_text='CO2 emissions per capita (metric tonnes)')
    
    return fig


def update_template(fig):
    '''
        Updates the layout of the figure, setting
        its template to 'simple_white'

        Args:
            fig: The figure to update
        Returns
            The updated figure
    '''
    # TODO : Update template
    fig.update_layout(template='simple_white')
    
    return fig


def update_legend(fig):
    '''
        Updated the legend title

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    # TODO : Update legend
    fig.update_layout(legend_title_text='Legend')
    return fig
