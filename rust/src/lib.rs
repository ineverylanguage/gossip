extern crate protobuf;

// Protobuf generated files
mod proto_client;

/// A versioned asset to be sycned via a gossip
pub trait Versioned {

  /// Returns the version number of the asset
  fn version(&self) -> i32;
}

/// Can reconcile a conflict between two versions of the asset
pub trait HasMerge {
  /// resolve the conflict between two versions of the asset
  fn merge(&self, other: &Self) -> Self;
}

/// Wrap a type as a versioned asset
pub struct WithVersion<T> {
  _version: i32,
  pub value: T
}

impl<T: Clone> WithVersion<T> {
  /// Create a new Versioned asset, setting the version to 0
  pub fn new(value: &T) -> WithVersion<T> {
    WithVersion::<T> { _version: 0, value: value.clone() }
  }

  /// Create a new Versioned asset with a specific version
  pub fn new_with_version(value: &T, v: i32) -> WithVersion<T> {
    WithVersion::<T> { _version: v, value: value.clone() }
  }

  /// Increment the asset with the next version number and a new value
  pub fn next(&self, value: &T) -> WithVersion<T> {
    WithVersion::<T> { _version: self._version + 1, value: value.clone() }
  }
}

/// Default Implementation of Versioned
impl<T> Versioned for WithVersion<T> {
  fn version(&self) -> i32 {
    self._version
  }
}

impl<T> HasMerge for T
    where T: Versioned + Clone {

    /// If self.version < other.version then self else other
    fn merge(&self, other: &Self) -> Self {
    match self.version() < other.version() {
      true => self.clone(),
      false => other.clone()
    }
  }
}
