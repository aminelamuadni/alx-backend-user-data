#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user with email and hashed password to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object if successful, None otherwise.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find and return the first user matching the provided search criteria
        using a compound tuple query.

        Args:
            **kwargs: Arbitrary keyword arguments corresponding to the User
                      model's attributes.

        Returns:
            User: The first User object that matches the criteria.

        Raises:
            NoResultFound: If no results are found that match the criteria.
            InvalidRequestError: If the query arguments are incorrect or
                                 invalid.
        """
        attributes, values = [], []
        for attribute, value in kwargs.items():
            if hasattr(User, attribute):
                attributes.append(getattr(User, attribute))
                values.append(value)
            else:
                raise InvalidRequestError()

        result = self._session.query(User).filter(
            tuple_(*attributes).in_([tuple(values)])
        ).first()

        if result is None:
            raise NoResultFound()

        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes based on user_id and given keyword
        arguments.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing the attributes
                      to update.

        Raises:
            ValueError: If any provided attribute name does not exist on the
                        User model.
            NoResultFound: If no user is found with the provided user_id.
        """
        user = self.find_user_by(id=user_id)
        if not user:
            raise NoResultFound()

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError()

        self._session.commit()
