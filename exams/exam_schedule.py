import csv
import re

def process_exam_schedule(csv_file):
    """
    Processes a CSV file containing an exam schedule and outputs a formatted plain text representation.

    Args:
        csv_file (str): The path to the CSV file.
    """

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    output = ""
    for i in range(0, len(data)):
        line = data[i]
        
        if not line:
            continue

        if "April" in line[0]:
            day = line[0].replace(",", "")
            output += f"{day} schedule\n"

        if "COMP" in line[0]:
            exam_details = line[0]
            proctors = line
            rooms = data[i-1]

            # Extract course code and instructor
            match = re.search(r'(COMP \d+)\s*\(([^)]+)\)', exam_details)
            if match:
                course_code = match.group(1)
                instructor = match.group(2)
                
                #Extract exam time
                time_match = re.search(r'Exam time\s*(\d+)-\d+([ap]m)', exam_details)
                if time_match:
                  exam_time = time_match.group(1).strip()
                  exam_time += time_match.group(2).strip()
                  output += f"{exam_time} - {course_code} - {instructor}\n"

                # Assign proctors to rooms
                for j in range(1, len(rooms)):
                    if rooms[j] != '':
                        proctor_name = proctors[j] if j < len(proctors) else "Not Assigned" #Safeguard against index out of bounds error
                        output += f"{rooms[j]}\t{proctor_name}\n"
                output += "\n"

    return output

# Example usage (replace "exam_schedule.csv" with the actual file name)
if __name__ == "__main__":
    formatted_output = process_exam_schedule("exams.csv")  # Replace with your file name
    print(formatted_output)