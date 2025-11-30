"""Módulo contendo a classe base de repositório."""

from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    Repositório base genérico para operações CRUD.
    
    Attributes:
        model: Classe do modelo SQLAlchemy.
        session: Sessão do banco de dados.
    """
    
    def __init__(self, model: type, session: Session):
        """
        Inicializa o repositório.
        
        Args:
            model: Classe do modelo.
            session: Sessão do SQLAlchemy.
        """
        self.model = model
        self.session = session
    
    def create(self, entity: T) -> T:
        """
        Cria uma nova entidade no banco de dados.
        
        Args:
            entity: Entidade a ser criada.
            
        Returns:
            Entidade criada com ID atribuído.
        """
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        Busca uma entidade por ID.
        
        Args:
            entity_id: ID da entidade.
            
        Returns:
            Entidade encontrada ou None.
        """
        return self.session.query(self.model).filter(self.model.id == entity_id).first()
    
    def get_all(self) -> List[T]:
        """
        Retorna todas as entidades.
        
        Returns:
            Lista de entidades.
        """
        return self.session.query(self.model).all()
    
    def update(self, entity: T) -> T:
        """
        Atualiza uma entidade existente.
        
        Args:
            entity: Entidade a ser atualizada.
            
        Returns:
            Entidade atualizada.
        """
        self.session.commit()
        self.session.refresh(entity)
        return entity
    
    def delete(self, entity: T) -> None:
        """
        Remove uma entidade do banco de dados.
        
        Args:
            entity: Entidade a ser removida.
        """
        self.session.delete(entity)
        self.session.commit()
