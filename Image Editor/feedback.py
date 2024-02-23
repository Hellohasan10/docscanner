# feedback.py
import os
from datetime import datetime
from flask import Blueprint, request, jsonify

# Create a Blueprint for feedback-related routes
feedback_bp = Blueprint('feedback_bp', __name__)

# Function to save feedback
def save_feedback(rating, comment):
    # Ensure the feedback directory exists
    feedback_dir = 'feedback'
    if not os.path.exists(feedback_dir):
        os.makedirs(feedback_dir)
    
    # Create a timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'feedback_{timestamp}.txt'
    
    # Write the rating and comment to the file
    filepath = os.path.join(feedback_dir, filename)
    with open(filepath, 'w') as f:
        f.write(f'Rating: {rating}\nComment: {comment}\n')

# Route to handle feedback submissions
@feedback_bp.route('/submit-feedback', methods=['POST'])
def handle_feedback():
    data = request.json
    rating = data['rating']
    comment = data['comment']
    
    # Save the feedback
    save_feedback(rating, comment)
    
    # Return a success response
    return jsonify({'status': 'success', 'message': 'Thank you for your feedback!'})

# Add other feedback-related routes or functionality here if necessary
