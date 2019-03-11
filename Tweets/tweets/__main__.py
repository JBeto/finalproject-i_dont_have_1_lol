import tweets.streams as streams


output_file = open('data.txt', 'w')


def read_data(data):
    # filter out deleted tweets
    if 'created_at' in data and data['place'] is not None:
        output_file.write(str(data))
        output_file.write('\n')


streams.stream_data(read_data)
output_file.close()
