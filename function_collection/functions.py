def Hot_encoding(DataFrame, Column_name, sep='; ', dropna=True, threading=False, df_dict=None):
    item_set = set()

    def Unique_element_in_series(item):
        if item is np.nan:
            pass
        else:
            item_list = item.split("; ")
            item_set.update(item_list)

    if (dropna == True):
        Column_series = DataFrame[Column_name].dropna()
        Column_series.apply(Unique_element_in_series)
    else:
        Column_series = DataFrame[Column_name]

    New_dict = dict()
    for i in item_set:
        New_dict[i] = np.zeros(Column_series.shape)
    Hot_encoded_df = pd.DataFrame(data=New_dict, index=Column_series.index, dtype=np.int8, )
    for i in tqdm_notebook(Column_series.index):
        item_list = Column_series.loc[i].split(sep)
        for item in item_list:
            Hot_encoded_df[item].loc[i] = 1
    if threading == True:
        df_list[Column_name] = Hot_encoded_df
    else:
        return Hot_encoded_df


def Hot_encoding_multi_threading(DataFrame, Column_names, sep='; ', dropna=True, df_dict=None):
    from threading import Thread
    threads = []
    for Column_name in Column_names:
        threads.append(
            Thread(target=Hot_encoding, args=(DataFrame, Column_name,),
                   kwargs={"threading": True, "df_dict": df_dict}))
    for thread in threads:
        thread.start()
    return df_dict


def Drop_zeros(Dataframe, column_name):
    return Dataframe[column_name][Dataframe[column_name] != 0]


# value_counts()와 비슷한 기능
def count_each_item_in_Series(Series, sep='; '):
    Language_list = []
    for items in Series:
        item_list = items.split(sep)
        for item in item_list:
            Language_list.append(item)
    Unique_item_set = set(Language_list)
    Language_numbers = []
    for Unique_item in Unique_item_set:
        Language_numbers.append(Language_list.count(Unique_item))
    return pd.Series(Language_numbers, index=Unique_item_set)


def language_plot(dictionary, column_name, kind='Pie'):
    fig, ax = plt.subplots(4, 2, figsize=(12, 16))
    fig.suptitle(column_name, fontsize=30, horizontalalignment='center', verticalalignment='baseline')
    plot_dict = dictionary[column_name]
    count = 0
    if kind == 'Pie':

        for key in plot_dict.keys():
            x_count, y_count = divmod(count, 2)
            Series = plot_dict[key].sort_values(ascending=False)[:5]
            labels = Series.index
            total_number = Series.sum()
            sizes = Series.apply(lambda x: int(x / total_number * 100))
            ax[x_count, y_count].pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True)
            ax[x_count, y_count].set_title(key)
            count += 1

    elif kind == 'Barh':
        plt.subplots_adjust(wspace=0.6)
        for key in plot_dict.keys():
            x_count, y_count = divmod(count, 2)
            Series = plot_dict[key].sort_values(ascending=True)[-5:]
            labels = Series.index
            ax[x_count, y_count].barh(labels, Series, align='center', height=0.5)
            ax[x_count, y_count].set_yticks(labels)
            ax[x_count, y_count].set_title(key)
            count += 1
    else:
        pass
    plt.show()


def plot_bar_chart_about_language_per_dev(Dict, Type, labels):
    fig = go.Figure(go.Bar(x=x, y=Dict[Type][labels[0]]['value'], name=labels[0],
                           hovertemplate=Dict[Type][labels[0]]['index'], text=Dict[Type][labels[0]]['index'],
                           textposition='auto',
                           marker=dict(color='rgb(158,202,225)', line=dict(color='rgb(8,48,107)', width=1.5),
                                       opacity=0.6)))
    for label in labels[1:]:
        color = 'rgb' + str((np.random.randint(255), np.random.randint(255), np.random.randint(255)))
        fig.add_trace(go.Bar(x=x, y=Dict[Type][label]['value'], name=label,
                             hovertemplate=Dict[Type][label]['index'], text=Dict[Type][label]['index'],
                             textposition='auto',
                             marker=dict(color=color, line=dict(color='rgb(8,48,107)', width=1.5), opacity=0.6)))
    fig.update_layout(barmode='stack')
    fig.show()