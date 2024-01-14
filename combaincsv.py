import csv
import shutil
import os

def combine_csv_files():
    def combine_csv_by_rows(input_files, output_file):
        temp_files = []
        for index, file in enumerate(input_files, start=1):
            temp_file = f'temp_{index}.csv'
            shutil.copyfile(file, temp_file)
            temp_files.append(temp_file)

        with open(output_file, 'w', newline='') as output_csv:
            writers = []
            for temp_file in temp_files:
                csv_file = open(temp_file, 'r')
                reader = csv.reader(csv_file)
                header = next(reader, [])
                if len(header) < 2:
                    print(f"CSV file {temp_file} should have at least two columns.")
                    csv_file.close()
                    continue
                writers.append((header, reader, csv_file))

            # Combine the headers from all CSV files to create the new header for the output CSV
            new_header = ["Time", *[header[1] for header, _, _ in writers]]
            writer = csv.writer(output_csv)
            writer.writerow(new_header)

            data_dicts = [{} for _ in range(len(writers))]
            for i, (header, reader, csv_file) in enumerate(writers):
                for row in reader:
                    if len(row) >= 2:
                        time, value = row[0], row[1]
                        data_dicts[i][time] = value
                csv_file.close()

            for time_entry in sorted(set(time for data_dict in data_dicts for time in data_dict)):
                row_data = [time_entry]
                for data_dict in data_dicts:
                    value = data_dict.get(time_entry, '0')
                    row_data.append(value)
                writer.writerow(row_data)

        # Close all the temporary files and delete them
        for _, _, csv_file in writers:
            csv_file.close()

        # Delete the temporary files
        for temp_file in temp_files:
            os.remove(temp_file)

        print(f"{len(input_files)} CSV files are combined into {output_file}.")


    # Usage example:
    input_files = [file for file in os.listdir() if file.endswith(".csv")]
    combine_csv_by_rows(input_files, 'combined_output.csv')

