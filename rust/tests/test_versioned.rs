extern crate gossip;
use gossip::Versioned;

mod mock {
	#[derive(Debug)]
	pub struct TestItem {
	  pub i: i32
	}

	impl Clone for TestItem {
	  fn clone(&self) -> Self {
	    TestItem { i: self.i }
	  }
	}

	impl PartialEq for TestItem {
		fn eq(&self, other: &Self) -> bool {
			self.i == other.i
		}
	}
}

#[test]
fn test_versioned() {
  let y = mock::TestItem { i: 32 };
  let x = gossip::WithVersion::new(&y);

  assert_eq!(x.value, y);
}

#[test]
fn test_versioned_next() {
	let y = mock::TestItem { i: 32 };
	let x = gossip::WithVersion::new(&y);
	let x_prime = x.next(&y);

	assert_eq!(x.version(), 0);
	assert_eq!(x_prime.version(), 1);
}
