from fastapi import HTTPException


def role_required(required_role):

    def checker(user):

        if user.get("role") != required_role:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return True

    return checker