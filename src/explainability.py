"""
Explainability Module
Visualize matching rationale and feature contributions
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def create_score_breakdown_chart(component_scores, weights):
    """
    Create a horizontal bar chart showing component scores and their weights
    """
    components = list(component_scores.keys())
    scores = [component_scores[comp] for comp in components]
    weight_values = [weights.get(comp, 0) * 100 for comp in components]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Component Scores (%)", "Weight Contribution (%)"),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Component scores
    fig.add_trace(
        go.Bar(
            y=components,
            x=scores,
            orientation='h',
            marker=dict(color=scores, colorscale='Viridis'),
            text=[f"{s}%" for s in scores],
            textposition='auto',
            name='Score'
        ),
        row=1, col=1
    )
    
    # Weight contributions
    fig.add_trace(
        go.Bar(
            y=components,
            x=weight_values,
            orientation='h',
            marker=dict(color='lightblue'),
            text=[f"{w}%" for w in weight_values],
            textposition='auto',
            name='Weight'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_text="Match Score Breakdown"
    )
    
    fig.update_xaxes(range=[0, 100])
    
    return fig


def create_radar_chart(component_scores):
    """Create a radar chart for component scores"""
    components = list(component_scores.keys())
    scores = [component_scores[comp] for comp in components]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=components,
        fill='toself',
        name='Candidate Score',
        marker=dict(color='rgb(99, 110, 250)')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title="Candidate Profile Radar"
    )
    
    return fig


def create_skills_overlap_chart(candidate_skills, job_skills):
    """
    Visualize skills overlap between candidate and job requirements
    """
    candidate_set = set([s.lower() for s in candidate_skills])
    job_set = set([s.lower() for s in job_skills])
    
    matched_skills = candidate_set.intersection(job_set)
    missing_skills = job_set - candidate_set
    extra_skills = candidate_set - job_set
    
    # Create data for visualization
    categories = []
    skills_list = []
    colors = []
    
    for skill in matched_skills:
        categories.append('Matched')
        skills_list.append(skill.title())
        colors.append('green')
    
    for skill in missing_skills:
        categories.append('Missing')
        skills_list.append(skill.title())
        colors.append('red')
    
    for skill in list(extra_skills)[:5]:  # Limit extra skills
        categories.append('Additional')
        skills_list.append(skill.title())
        colors.append('blue')
    
    # Create summary
    summary = {
        'matched': len(matched_skills),
        'missing': len(missing_skills),
        'additional': len(extra_skills),
        'match_percentage': round(len(matched_skills) / len(job_set) * 100, 1) if job_set else 0
    }
    
    return summary, {
        'categories': categories,
        'skills': skills_list,
        'colors': colors
    }


def create_ranking_chart(matches, top_n=10):
    """
    Create a bar chart showing top N candidates
    """
    top_matches = matches[:top_n]
    
    names = [m['candidate_name'] for m in top_matches]
    scores = [m['overall_score'] for m in top_matches]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=scores,
        y=names,
        orientation='h',
        marker=dict(
            color=scores,
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Score %")
        ),
        text=[f"{s}%" for s in scores],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Top Candidates Ranking",
        xaxis_title="Match Score (%)",
        yaxis_title="Candidate",
        height=max(400, top_n * 40),
        yaxis=dict(autorange="reversed")
    )
    
    fig.update_xaxes(range=[0, 100])
    
    return fig


def create_comparison_heatmap(matches):
    """
    Create a heatmap comparing all candidates across different criteria
    """
    if not matches:
        return None
    
    candidates = [m['candidate_name'] for m in matches]
    components = list(matches[0]['component_scores'].keys())
    
    # Build matrix
    matrix = []
    for match in matches:
        row = [match['component_scores'][comp] for comp in components]
        matrix.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=components,
        y=candidates,
        colorscale='Viridis',
        text=matrix,
        texttemplate='%{text:.1f}%',
        textfont={"size": 10},
        colorbar=dict(title="Score %")
    ))
    
    fig.update_layout(
        title="Candidate Comparison Heatmap",
        xaxis_title="Criteria",
        yaxis_title="Candidate",
        height=max(400, len(candidates) * 30)
    )
    
    return fig


def generate_explanation_text(match_result, job):
    """
    Generate human-readable explanation for the match
    """
    score = match_result['overall_score']
    name = match_result['candidate_name']
    components = match_result['component_scores']
    
    # Determine overall assessment
    if score >= 80:
        assessment = "**Excellent Match** 🌟"
        recommendation = "Highly recommended for interview"
    elif score >= 65:
        assessment = "**Good Match** ✅"
        recommendation = "Recommended for consideration"
    elif score >= 50:
        assessment = "**Moderate Match** ⚠️"
        recommendation = "May require additional evaluation"
    else:
        assessment = "**Weak Match** ❌"
        recommendation = "Not recommended for this position"
    
    # Build explanation
    explanation = f"""
### Match Assessment for {name}

**Overall Score**: {score}%  
**Assessment**: {assessment}  
**Recommendation**: {recommendation}

---

#### Score Breakdown:

- **Skills Match**: {components['skills']}%
  - {"Strong alignment with required skills" if components['skills'] >= 70 else "Partial skills match - may need training"}

- **Experience**: {components['experience']}%
  - {"Meets or exceeds experience requirements" if components['experience'] >= 80 else "Some experience gap identified"}

- **Education**: {components['education']}%
  - {"Education level matches requirements" if components['education'] >= 80 else "Education level below preferred"}

- **Location**: {components['location']}%
  - {"Location compatible" if components['location'] >= 70 else "Location may require relocation/remote work"}

---

#### Key Strengths:
"""
    
    # Add strengths
    strengths = []
    if components['skills'] >= 70:
        strengths.append("- Strong technical skills alignment")
    if components['experience'] >= 80:
        strengths.append("- Extensive relevant experience")
    if components['education'] >= 80:
        strengths.append("- Appropriate education background")
    
    if strengths:
        explanation += "\n".join(strengths)
    else:
        explanation += "- Consider for growth potential"
    
    # Add areas for consideration
    explanation += "\n\n#### Areas for Consideration:\n"
    
    considerations = []
    if components['skills'] < 70:
        considerations.append("- Skills gap may require training")
    if components['experience'] < 70:
        considerations.append("- Limited experience in required areas")
    if components['education'] < 70:
        considerations.append("- Education level below preferred")
    
    if considerations:
        explanation += "\n".join(considerations)
    else:
        explanation += "- No major concerns identified"
    
    return explanation


def get_matching_keywords(candidate_skills, job_skills):
    """Extract matching keywords between candidate and job"""
    candidate_set = set([s.lower() for s in candidate_skills])
    job_set = set([s.lower() for s in job_skills])
    
    matched = list(candidate_set.intersection(job_set))
    return [s.title() for s in matched]
