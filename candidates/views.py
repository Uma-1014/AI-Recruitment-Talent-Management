from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ai_engine.resume_parser import parse_resume

from .forms import CandidateForm
from .models import Candidate


@login_required
def profile(request):

    candidate, created = Candidate.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': (
                request.user.get_full_name()
                or request.user.username
            ),
            'email': request.user.email or '',
        }
    )

    if request.method == 'POST':

        form = CandidateForm(
            request.POST,
            request.FILES,
            instance=candidate
        )

        if form.is_valid():

            candidate = form.save(
                commit=False
            )

            candidate.user = request.user

            candidate.save()

            # ==========================================
            # AI RESUME ANALYSIS
            # ==========================================

            if candidate.resume:

                try:

                    resume_data = parse_resume(
                        candidate.resume.path
                    )

                    # ----------------------------------
                    # Automatically extracted email
                    # ----------------------------------

                    if resume_data.get('email'):

                        candidate.email = (
                            resume_data['email']
                        )

                    # ----------------------------------
                    # Automatically extracted phone
                    # ----------------------------------

                    if resume_data.get('phone'):

                        candidate.phone = (
                            resume_data['phone']
                        )

                    # ----------------------------------
                    # Automatically extracted skills
                    # ----------------------------------

                    skills = resume_data.get(
                        'skills',
                        []
                    )

                    if skills:

                        candidate.skills = (
                            ', '.join(skills)
                        )

                    # ----------------------------------
                    # Automatically extracted experience
                    # ----------------------------------

                    experience = resume_data.get(
                        'experience_years'
                    )

                    if experience is not None:

                        candidate.experience_years = (
                            experience
                        )

                    # ----------------------------------
                    # Automatically extracted education
                    # ----------------------------------

                    education = resume_data.get(
                        'education',
                        []
                    )

                    if education:

                        candidate.education = (
                            ', '.join(education)
                        )

                    candidate.save()

                    messages.success(
                        request,
                        'Resume uploaded and analyzed successfully by AI.'
                    )

                except Exception as error:

                    messages.warning(
                        request,
                        'Resume uploaded, but AI analysis '
                        'could not extract all information.'
                    )

                    print(
                        'Resume parsing error:',
                        error
                    )

            else:

                messages.success(
                    request,
                    'Candidate profile updated successfully.'
                )

            return redirect(
                'candidate_profile'
            )

    else:

        form = CandidateForm(
            instance=candidate
        )

    return render(
        request,
        'candidates/profile.html',
        {
            'form': form,
            'candidate': candidate,
        }
    )