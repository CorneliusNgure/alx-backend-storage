#!/usr/bin/env python3
"""
Returns all students sorted by average score from a
MongoDB collection.
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score from a
    MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The pymongo collection object.

    Returns:
        list: A list of dictionaries, each containing the
        student's data and their average score, sorted by
        average score in descending order.
    """
    # Fetch all students from the collection
    students = mongo_collection.find()
    
    # Prepare a list to hold student data with average scores
    student_scores = []
    
    for student in students:
        # Calculate the average score
        topics = student.get('topics', [])
        if not topics:
            average_score = 0
        else:
            total_score = sum(topic['score'] for topic in topics)
            average_score = total_score / len(topics)
        
        # Create a dictionary with student ID, name, and average score
        student_scores.append({
            '_id': student['_id'],
            'name': student['name'],
            'averageScore': average_score
        })
    
    # Sort the list of students by average score in descending order
    sorted_students = sorted(student_scores, key=lambda x: x['averageScore'], reverse=True)
    
    return sorted_students
